'''
This files parses the translation notes AFTER they have been 
formatted using proskomma. 

This script
- reads the files
- create a translation note for a specific unique id
- then links that translation note to the source text
'''

import glob
import os
import pandas as pd
from sqlalchemy import create_engine

inputfiles = glob.glob('../proskomma/src/scripts/*Parsed.tsv')
dataframes = []

for inputfile in inputfiles:
    try:
        df = pd.read_csv(inputfile, sep="\t")
        if df.shape[0] > 0:
            dataframes.append(df)
    except pd.errors.EmptyDataError:
        print(f'There is no data in {inputfile}')


df = pd.concat(dataframes)

filenames = {
         os.path.basename(inputfile).replace('Parsed.tsv', '').replace('en_tn_', '').split('-')[-1]: os.path.basename(inputfile).replace('Parsed.tsv', '').replace('en_tn_', '')
    for inputfile in inputfiles
    }
df.book = df.book.map(filenames)
print(df)

# There are a lot of notes without a supportReference
df.loc[df.supportReference.isnull()]

# Many notes are repeated as they are linked to every source language word they 
# are linked to. This should form the basis for a ForeignKey (ManyToOne) link.
df.noteID.value_counts()

# create the notes table
df.groupby('noteID').first().reset_index()

# sample query
df.groupby('noteID').first().loc['scr8']

engine = create_engine('sqlite:///../project_lexicon/alignment.db', echo=False)
df.groupby('noteID').first().reset_index().to_sql('notes', con=engine, if_exists='replace')


# Now link the notes and the source words
# This needs to be a many2many relationship so that it is possible
# to link multiple words to a note and multiple notes to a word
source = pd.read_csv('../data/alignment/source.csv')
print(source)

short_source = source['id token book chapter verse occ'.split()]
short_df = df['noteID sourceWord book chapter verse sourceWordOccurrence'.split()]

short_source.token = short_source.token.str.strip()
m2m = short_df.merge(short_source, left_on='book chapter verse sourceWord sourceWordOccurrence'.split(), right_on='book chapter verse token occ'.split())



m2m.columns = 'notes_id source_word book chapter verse occ source_id token occ_bis'.split()
m2m.to_sql('notesM2M', con=engine, if_exists='replace')