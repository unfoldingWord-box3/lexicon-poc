
import re
import sys
import os

import pandas as pd
import spacy

df_full = pd.read_csv('data/alignment/ult.csv')

# fields to extract: occ, occs, nrOfTargetWords, nrOfSourceWords


## get source text phrases
source_blocks = df_full.groupby('alg_id').first()
source_blocks = source_blocks.explode('alg')  # do not ignore the index
source_blocks = source_blocks.assign(source_token=source_blocks.alg.str.extract(r'x-content=\"(.*?)\"'))
source_blocks_dict = source_blocks.groupby('alg_id').apply(lambda x: ' '.join(x.source_token.fillna(''))).to_dict()
df_full = df_full.assign(source_blocks=df_full.alg_id.map(source_blocks_dict))

# NB: discard the rows *without* alignment
df_full = df_full.loc[df_full.token != '',:]
print(df_full)

df = df_full.loc[df_full.alg.isnull()==False,:]
# df = df.loc[df.token != '',:]

# Change float to int 
# df['alg_id'] = df['alg_id'].astype(int)

## There are cases where an alignment is interrupted
# find cases where the alignment id is different, 
# but the entire alignment group is the same
# the selected alignment id's should actually be given the same
# future versions of this script could include indicating a gap 
# The example that triggered this code is 
#   'as X reclined to eat' (cf. Mat 9:10)
# To retrieve it, use `df.loc[(df.chapter == '9') & (df.verse == '10')]`

df['sample_alg_str'] = df.alg.astype(str)
need_to_be_merged = df.groupby('chapter verse sample_alg_str'.split()).alg_id.unique()
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

## There are cases with embedded alignment
df.loc[:, 'nrOfAlg'] = df.alg.fillna('').apply(len)
df.loc[df.nrOfAlg > 1]

# Extract the target data
df = df.assign(target_token=df.token.str.extract(r'\w( .*?)\|'))
df = df.assign(target_token_prefix=df.token.str.strip().str.extract(r'(.*?)(\\w)m( .*?)\|')[0])  # this selects the first group, viz. whatever occurs *before* \w
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

have_gaps = df.loc[df.alg_id.isin(merging.values())].groupby('alg_id').apply(lambda x: find_gaps(x.index.tolist()))
need_gap_highlighting = [i for itm in have_gaps.tolist() for i in itm]
df.loc[:,'alg_has_gap'] = False
df.loc[need_gap_highlighting, 'alg_has_gap'] = True
# df.to_excel('./data/alignment/target.xlsx')  # CAREFUL: this only exports THOSE TOKENS WITH AN ALIGNMENT
df.to_csv('./data/alignment/target.csv')  # CAREFUL: this only exports THOSE TOKENS WITH AN ALIGNMENT

# do this after so the export above is still clear
df.loc[df.alg_has_gap, 'target_token'] = df.loc[df.alg_has_gap, 'target_token'] + ' … '

# move each element in the `alg` array to a separate row
# ignore index avoids copying the index of a row that is exploded
df = df.explode('alg', ignore_index=True)

# Extract the source data
df = df.assign(strongs=df.alg.str.extract(r'x-strong=\"(.*?)\"'))
df = df.assign(lemma=df.alg.str.extract(r'x-lemma=\"(.*?)\"'))
df = df.assign(morph=df.alg.str.extract(r'x-morph=\"(.*?)\"'))
df = df.assign(source_token=df.alg.str.extract(r'x-content=\"(.*?)\"'))
df = df.assign(source_occ=df.token.str.extract(r'x-occurrence=\"(.*?)\"'))
df = df.assign(source_occs=df.token.str.extract(r'x-occurrences=\"(.*?)\"'))
df.loc[:, 'hasPrefix'] = False
df.loc[df.strongs.str.contains(r'd:|c:|l:|i:|k:|b:|m:').fillna(False), 'hasPrefix'] = True
df.loc[:, 'strongsNoPrefix'] = df.strongs.str.strip('d:|c:|l:|i:|k:|b:|m:')

## df.to_excel('./data/alignment/alignment.xlsx')
df.to_csv('./data/alignment/alignment.csv')

# Do some analysis


# phrase alignments
target_tokens = df.groupby('strongs alg_id'.split()).apply(lambda x: x.target_token.fillna('').sum())
target_tokens.shape
# get the lemma
lemmata = df.groupby('strongs alg_id'.split()).lemma.first()
source_tokens = df.groupby('strongs alg_id'.split()).source_token.first()
source_blocks = df.groupby('strongs alg_id'.split()).source_blocks.first()

allinone = pd.concat([target_tokens, lemmata, source_tokens, source_blocks], axis=1)
allinone.rename(columns={0:'target_blocks'}, inplace=True)

# choose a root for each alignment
nlp = spacy.load("en_core_web_sm")

def parse(input_string):
    output = []
    doc = nlp(input_string)
    for token in doc:
        output.append([token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                token.shape_, token.is_alpha, token.is_stop])
    return pd.DataFrame(output, columns='token lemma pos tag dep shape is_alpha is_stop'.split())

roots = []
for itm in allinone.target_blocks.tolist():
    parsing = parse(itm)
    # print()
    # print(parsing.loc[parsing.dep == 'ROOT', 'lemma'].tolist(), itm)
    roots.append(parsing.loc[parsing.dep == 'ROOT', 'lemma'].tolist()[0])
allinone['roots'] = roots

dense = allinone.groupby('strongs target_blocks'.split()).size()
dense
allinone.groupby('strongs target_blocks'.split()).size()
allinone.groupby('strongs source_blocks target_blocks'.split()).size().head(60)

allinone.to_csv('./data/alignment/dictionary.csv')
## allinone.to_excel('./data/alignment/dictionary.xlsx')

# get the counts for each sense
counts = allinone.groupby(['strongs', 'target_blocks']).size()
## counts.to_excel('./data/alignment/counts.xlsx')
counts.to_csv('./data/alignment/counts.csv')
counts.head(50)







# query a strongs number
allinone.loc['G00180']

# find synonyms
allinone.loc[allinone['target_blocks'].str.contains('bad')]
allinone.loc[allinone['target_blocks'].str.contains('said')].lemma.value_counts()

# IDEA
# if a word is aligned with many different strongs numbers, surely it is a function word
# I could doc frequency to identify these function words

# alternatively
# you could re-align these using a pre-trained aligner? 
# or you could start with cases without any prefixes
df.loc[df.alg.str.get(0).fillna('').str.contains('c:H0559')].target_token.str.upper().value_counts()

# how do you group the entries into senses?

# more query examples
kings = df.loc[df.alg.fillna('').str.contains('H4428')]
kings.source_token.str.upper().value_counts()
kings.target_token.str.upper().value_counts()

# for אֵת this does not work
df.loc[df.alg.str.get(0).fillna('').str.contains('H0853')].target_token.str.upper().value_counts()

# son / sons , my/your/his/a
df.loc[df.alg.str.get(0).fillna('').str.contains('H1121a')].target_token.str.upper().value_counts()

df.loc[df.strongsNoPrefix == 'H0559'].target_token.str.upper().value_counts()
df.loc[-df.hasPrefix]





# IDEAS
# we are going to find a lot of alignment mistakes, maybe even translation mistakes
# ideally we could develop a memory-based or a dictionary-based alignment
# can I create a tool that automatically
# 1. uses synonyms to make a translation more dynamic
# 2. a webapp that reads ufsm files and transforms them to tsv


# compare the frequencies to find the headwords
# compare the document frequency

# get the metaphorical usages based on translationWords or figs-