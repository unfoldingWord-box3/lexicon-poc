import glob
import subprocess
import os

import pandas as pd


# CONVERT USFM FILES TO CSV

ult_files = glob.glob('./data/en_ult/*.usfm')

# for ipf in ult_files:
#     print(f'Processing {ipf}')
#     basename = os.path.basename(ipf).replace('usfm', 'csv')
#     subprocess.call(['python', 'ult2csv.py', ipf, f'data/alignment/en_ult_csv/{basename}'])


# MERGE MULTIPLE CSV FILES INTO A SINGLE ONE
ult_csv_files = sorted(glob.glob('./data/alignment/en_ult_csv/*.csv'))

dataframes = []
for ipf in ult_csv_files:
    dataframes.append(pd.read_csv(ipf))
df = pd.concat(dataframes)

df = df.reset_index(drop=True) 
df = df.rename(columns={'Unnamed: 0':'orig_id'})
df.to_csv('data/alignment/ult.csv')