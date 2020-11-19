import glob
import subprocess
import os

import pandas as pd


# CONVERT USFM ULT FILES TO CSV
ult_files = glob.glob('./data/en_ult/*.usfm')

for ipf in ult_files:
    print(f'Processing {ipf}')
    basename = os.path.basename(ipf).replace('usfm', 'csv')
    subprocess.call(['python', 'ult2csv.py', ipf, f'data/alignment/en_ult_csv/{basename}'])


# MERGE MULTIPLE ULT CSV FILES INTO A SINGLE ONE
ult_csv_files = sorted(glob.glob('./data/alignment/en_ult_csv/*.csv'))

dataframes = []
for ipf in ult_csv_files:
    dataframes.append(pd.read_csv(ipf))
df = pd.concat(dataframes)

df = df.reset_index(drop=True) 
df = df.rename(columns={'Unnamed: 0':'orig_id'})
df.to_csv('data/alignment/ult.csv')
df.to_pickle('data/alignment/ult.pickle')


# CONVERT SOURCES FILES TO CSV
hebrew_files = glob.glob('./data/hbo_uhb/*.usfm')
greek_files = glob.glob('./data/el-x-koine_ugnt/*.usfm')
sources_files = hebrew_files + greek_files

for ipf in sources_files:
    print(f'Processing {ipf}')
    basename = os.path.basename(ipf).replace('usfm', 'csv')
    subprocess.call(['python', 'source2csv.py', ipf, f'data/alignment/source_csv/{basename}'])


# MERGE MULTIPLE SOURCE CSV FILES INTO A SINGLE ONE
source_csv_files = sorted(glob.glob('./data/alignment/source_csv/*.csv'))

dataframes = []
for ipf in source_csv_files:
    dataframes.append(pd.read_csv(ipf))
df = pd.concat(dataframes)

df = df.reset_index(drop=True) 
df = df.rename(columns={'Unnamed: 0':'orig_id'})
df.to_csv('data/alignment/source.csv')
df.to_pickle('data/alignment/source.pickle')