#!/usr/bin/env python
# coding: utf-8

import glob
import pandas as pd
import os

from engine import engine

inputfiles = glob.glob('../data/en_tq/*.tsv')

dataframes = []

for ipf in inputfiles:  
    df = pd.read_csv(ipf, sep='\t')
    basename = os.path.basename(ipf).replace('_tq.tsv', '')
    df['book'] = [basename] * df.shape[0]
    chapter_verse = df.Reference.str.split(':', expand=True)
    df['chapter'] = chapter_verse[0].astype(int)
    df['verse'] = chapter_verse[1].astype(int)
    dataframes.append(df)

df = pd.concat(dataframes)
df.reset_index(inplace=True, drop=True)

df.to_csv('../data/csv/tq.csv')
df.to_sql('question', con=engine, if_exists='replace')