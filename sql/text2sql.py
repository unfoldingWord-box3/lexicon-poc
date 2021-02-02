import re
import sys
import os

import pandas as pd
import spacy
from sqlalchemy import create_engine

# df stands for DataFrame
df = pd.read_csv('../data/alignment/ult.csv')
# or read the pickle
# df = pd.read_pickle('data/alignment/ult.pickle')

# discard empty tokens
df = df.loc[df.token != '',:]
df = df.loc[-df.token.isnull(),:]

# discard rows *without* alignment, this is a choice,
# one could also keep the entire target language text
df = df.loc[-df.alg.isnull(),:]

# The aligment is a list, but when it is written to csv or pickle it is coerced to a string.
# We need it to be a list.
# This hack here is what it is: evil eval. A future version, you know
# the one that is never going to be written, should store the data at 
# creation time as json.
# In my defense: eval is called here on data I trust. 

# Convert string to list
df.loc[-df.alg.isnull(), 'alg'] = df.loc[-df.alg.isnull()].alg.apply(eval)

# Get source text phrases
source_blocks = df.groupby('alg_id').first()
source_blocks = source_blocks.explode('alg')  # do not ignore the index
source_blocks = source_blocks.assign(source_token=source_blocks.alg.str.extract(r'x-content=\"(.*?)\"'))
source_blocks_dict = source_blocks.groupby('alg_id').apply(lambda x: ' '.join(x.source_token.fillna(''))).to_dict()
df = df.assign(source_blocks=df.alg_id.map(source_blocks_dict))

# There are cases where an alignment is interrupted.
# We want to insert an ellipsis where that is the case.
# Find cases where the alignment id is different, 
# but the entire alignment group is the same
# the selected alignment id's should actually be given the same
# future versions of this script could include indicating a gap 
# The example that triggered this code is 
#   'as X reclined to eat' (cf. Mat 9:10)
# To retrieve it, use `df.loc[(df.chapter == '9') & (df.verse == '10')]`

# Here we do need it to be a string, in order to group by unique alignments
df['sample_alg_str'] = df.alg.astype(str)
need_to_be_merged = df.groupby('book chapter verse sample_alg_str'.split()).alg_id.unique()
need_to_be_merged = need_to_be_merged[need_to_be_merged.apply(len) > 1].tolist()
merging = {}
for itm in need_to_be_merged:
    for element in itm[1:]:
        # for each element refer to the first occurrence of the alignment
        merging[element] = itm[0]
# store the original alignment id
df['alg_id_old'] = df['alg_id']
# merge these alg_id to make them a single one
df.loc[df['alg_id'].isin(merging.keys()), 'alg_id'] = df['alg_id'].map(merging)

# Extract the target data
df = df.assign(target_token=df.token.str.extract(r'\w( .*?)\|'))
df = df.assign(target_token_prefix=df.token.str.strip().str.extract(r'(.*?)(\\w)( .*?)\|')[0])  # this selects the first group, viz. whatever occurs *before* \w
df = df.assign(target_occ=df.token.str.extract(r'x-occurrence=\"(.*?)\"'))
df = df.assign(target_occs=df.token.str.extract(r'x-occurrences=\"(.*?)\"'))

# Highlight a gap with … 
def find_gaps(li):
    pairs = list(zip(li, li[1:]))
    has_gap = []
    for idx,itm in enumerate(pairs):
        if itm[1] - itm[0] > 1:
            has_gap.append(idx)
    return [li[i] for i in has_gap]

# this is dense: group by alignments, then identify where the gap/s is/are found
have_gaps = df.loc[df.alg_id.isin(merging.values())].groupby('alg_id').apply(lambda x: find_gaps(x.index.tolist()))
need_gap_highlighting = [i for itm in have_gaps.tolist() for i in itm]
df.loc[:,'alg_has_gap'] = False
df.loc[need_gap_highlighting, 'alg_has_gap'] = True

# use a temporary copy of the target token so that we can add the …
# for when we compute the target blocks
df['target_token_tmp'] = df.target_token
df.loc[df.alg_has_gap, 'target_token_tmp'] = df.loc[df.alg_has_gap, 'target_token'] + ' … '
target_tokens = df.groupby('alg_id'.split()).apply(lambda x: x.target_token_tmp.fillna('').sum())
df.loc[:, 'target_blocks'] = df.alg_id.map(target_tokens)

# clean some of the columns
df = df.drop('Unnamed: 0', axis=1)
df.loc[:, 'id'] = df.index.tolist()

# The goal is to split the data in three distinct tables:
# - Target (the gateway language or target language,
# in our case this is English)
# - Source (the source languages, which could be Greek or Hebrew/Aramaic, or any 
# language that is used to align to)
# - Alignment (links tokens in the Target and Source tables, and stores data pertaining 
# to the alignment itself, such as a unique id, and the target and source blocks)

target = df.loc[-df.token.isnull(), ['id', 'orig_id', 'token', 'chapter', 'verse',
   'book', 'alg_id', 'target_token', 'target_token_prefix', 'target_blocks',
   'target_occ', 'target_occs']]  # .reset_index(drop=True)

# CAREFUL: this only contains the tokens in Target WITH AN ALIGNMENT
# move each element in the `alg` array to a separate row
# ignore index avoids copying the index of a row that is exploded
backup = df.copy(deep=True)
df = df.explode('alg', ignore_index=True)
df = df.loc[-df.token.isnull(),:]

# Extract the source data, we'll need it to join the Alignment and Source tables
df = df.assign(source_token=df.alg.str.extract(r'x-content=\"(.*?)\"'))
df = df.assign(source_occ=df.alg.str.extract(r'x-occurrence=\"(.*?)\"'))
df = df.assign(source_occs=df.alg.str.extract(r'x-occurrences=\"(.*?)\"'))

# read the original Source file
source = pd.read_csv('../data/alignment/source.csv')

# add an ID column to Source
source = source.rename(columns={'id':'orig_id'})
source = source.rename(columns={'Unnamed: 0':'id'})

# tackle leading and trailing spaces
df.loc[df.source_token != df.source_token.str.strip()]
source.loc[source.token != source.token.str.strip()]
df['source_token_tmp'] = df['source_token'].str.strip()
source['token_tmp'] = source.token.str.strip()
# the dtypes of the columns differ, because one cannot coerce ints when they contains
# nans, I am using strings here. Bwerk. This is the stuff headaches are made of. 
source.occ = source.occ.astype(str)
source.occs = source.occs.astype(str)
# df.source_occ = df.source_occ.astype('Int64')
# source.occ = source.occ.astype('Int64')
# source.occ = source.occ.astype(object)
# source.occs = source.occs.astype(object)

# This is an INNER JOIN
# use `how='left'` for a LEFT OUTER JOIN, which would also include
# cases that cannot be linked to the source table
alignment = df.merge(source,
    left_on='book chapter verse source_token_tmp source_occ'.split(),
    right_on='book chapter verse token_tmp occ'.split())
alignment.loc[:, 'orig_id_x id_x id_y'.split()]

# example of a LEFT OUTER JOIN
left = df.merge(source,
    left_on='book chapter verse source_token_tmp source_occ'.split(),
    right_on='book chapter verse token_tmp occ'.split(), how='left')
left.loc[left.id_y.isnull()]
left.loc[left.id_y.isnull()].token_x.value_counts().tail(60)

# We want the following columns
# id (target), id (source), alg_id, alg, source_blocks, target_blocks, alg_has_gap
alignment = alignment.rename(columns={'id_x':'target_id', 'id_y':'source_id'})

# get a numerical alignment id, now that we have all alignments of all books,
# this will make indexing easier in the database
alignment_renumbering = dict(zip(alignment.alg_id.unique(), range(1, len(alignment.alg_id.unique())+1)))
alignment['alg_id_nr'] = alignment.alg_id.map(alignment_renumbering)
alignment['id'] = alignment.index.tolist()
alg = alignment['id target_id source_id alg_id alg alg_has_gap source_blocks target_blocks'.split()]

# example queries
example = alignment.loc[alignment.alg_id=='06-JOS-25']
target.loc[target.id.isin(example.target_id.tolist())]
source.loc[source.id.isin(example.source_id.tolist())]

example = alignment.loc[alignment.alg_id=='67-REV-10589']
target.loc[target.id.isin(example.target_id.tolist())]
source.loc[source.id.isin(example.source_id.tolist())]

example = source.loc[source.strongs=='H7225']
example_algs = alg.loc[alg.source_id.isin(example.id.tolist())]
target.loc[target.id.isin(example_algs.target_id.tolist())]

source = source[['id', 'index', 'source_token', 'book', 'chapter', 'verse', 'token',
       'token_prefix', 'morph', 'lemma', 'strongs', 'strongs_no_prefix', 'has_prefix',
       'translation_word', 'orig_id', 'occs', 'occ']]

counts = source.groupby('strongs_no_prefix').size()
source['strongs_count'] = source.strongs_no_prefix.map(counts).fillna(0).astype(int)

target.to_csv('../data/alignment/target.csv') 
# target.to_pickle('./data/alignment/target.pkl')

target.to_csv('../data/alignment/target.csv') 
alg.to_csv('../data/alignment/alignment.csv')
source.to_csv('../data/alignment/source.csv')

engine = create_engine('sqlite:///../project_lexicon/alignment.db', echo=False)

target.to_sql('target', con=engine, if_exists='replace')
alg.to_sql('alignment', con=engine, if_exists='replace')
source.to_sql('source', con=engine, if_exists='replace')

# engine.execute("SELECT * FROM users").fetchall()

engine.execute("SELECT * FROM target LIMIT 10").fetchall()
engine.execute("SELECT * FROM alignment LIMIT 10").fetchall() 