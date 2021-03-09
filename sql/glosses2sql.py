#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import glob
import os

from engine import engine

uhl_index = pd.read_json('../data/glosses/uhl/v0.1/index.json')
uhl_index.index = range(1, uhl_index.shape[0]+1)
uhl_files = glob.glob('../data/glosses/uhl/v0.1/content/*.json')

uhl_dataframes = []

for uhl_file in uhl_files:
    basename = os.path.basename(uhl_file)
    basename = basename.split('.')[0]
    df = pd.read_json(uhl_file, orient='index')
    df.columns = [int(basename)]
    uhl_dataframes.append(df)

uhl_data = pd.concat(uhl_dataframes, axis=1).T
uhl_data.sort_index(inplace=True)
uhl = pd.concat([uhl_index, uhl_data], axis=1)

uhl.to_csv('../data/csv/uhl_data.csv')

# Greek
ugl_files = glob.glob('../data/glosses/ugl/v0/content/*.json')
ugl_dataframes = []

for ugl_file in ugl_files:
    basename = os.path.basename(ugl_file)
    basename = basename.split('.')[0]
    df = pd.read_json(ugl_file, orient='index')
    df.columns = [int(basename)]
    ugl_dataframes.append(df)

ugl_data = pd.concat(ugl_dataframes, axis=1).T
ugl_data.sort_index(inplace=True)

ugl_data['id'] = ugl_data.index.tolist()
ugl_data['id'] = 'G' + ugl_data['id'].astype(str) + '0'
ugl = ugl_data

ugl.to_csv('../data/csv/ugl_data.csv')

# To SQL

uhl.columns = 'strongs lemma brief long'.split()
ugl.columns = 'brief long strongs'.split()

df = pd.concat([uhl[['strongs', 'brief', 'long', 'lemma']], ugl[['strongs', 'brief', 'long']]]).reset_index(drop=True)

df.to_sql('glosses', con=engine, if_exists='replace')