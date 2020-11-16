import re
import pandas as pd
import argparse
import sys
import os

from parse_utils import parse_usfm

# NOTE: this does not parse /k-s tags

parser = argparse.ArgumentParser(description='Parse a USFM text file and extract the alignment.')
# ipf = inputfile
parser.add_argument('ipf', help='provide a path to the file you want to parse', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
# ofp = outputfile
parser.add_argument('opf', help='provide a path to where you want to save the output', nargs='?', type=argparse.FileType('w'), default=sys.stdin)
args = parser.parse_args()
input_file = args.ipf.name
output_file = args.opf.name

try:
    os.path.exists(os.path.abspath(input_file))
    with open(input_file) as ipf: 
        contents = ipf.read()
except:
    print("The file %s does not exist!" % args.ipf)

# with open('./data/el-x-koine_ugnt/41-MAT.usfm') as ipf: 
# with open('./data/hbo_uhb/01-GEN.usfm') as ipf:     
#    contents = ipf.read()

print('There are {} tokens in the sample.'.format(len(contents.split())))

# Process the data 
words = parse_usfm(contents)
df_full = pd.DataFrame(words)
df_full.rename(columns={'token': 'source_token'}, inplace=True)

df = df_full.loc[df_full.source_token != '',:]
print(df.head(20))

# Extract the target data
df = df.assign(token=df.source_token.str.extract(r'\w( .*?)\|'))
df = df.assign(token_prefix=df.source_token.str.strip().str.extract(r'(.*?)(\\w)( .*?)\|')[0])  # this selects the first group, viz. whatever occurs *before* \w
df = df.assign(morph=df.source_token.str.extract(r'x-morph=\"(.*?)\"'))
df = df.assign(lemma=df.source_token.str.extract(r'lemma=\"(.*?)\"'))
df = df.assign(strongs=df.source_token.str.extract(r'strong=\"(.*?)\"'))
df.loc[:, 'has_prefix'] = False
df.loc[df.strongs.str.contains(r'd:|c:|l:|i:|k:|b:|m:').fillna(False), 'has_prefix'] = True
df.loc[:, 'strongs_no_prefix'] = df.strongs.str.strip('d:|c:|l:|i:|k:|b:|m:')
df = df.assign(translation_word=df.source_token.str.extract(r'x-tw=\"(.*?)\"'))

# store the id
df = df.assign(id=df.index.tolist())

# get the total number of occurrences
nr_occ_per_verse = df.groupby('chapter verse'.split()).token.value_counts()
nr_occ_per_verse.name = 'occs'
df = df.merge(nr_occ_per_verse, on='chapter verse token'.split())

# get the occurrence
exact_occ_per_verse = df.groupby('chapter verse token'.split()).cumcount() + 1
df = df.assign(occ=exact_occ_per_verse)

df = df.rename(columns={'Unnamed: 0':'id'})
df.index = df.id
df.index.name = 'index'
df = df.sort_values(by='index')

bookname = os.path.basename(input_file).replace('.usfm', '')
df = df.assign(book=[bookname]*df.shape[0])

print(df.head(20))

try:
    os.path.exists(os.path.abspath(output_file))
    # df.to_csv('./data/alignment/source.csv')
    df.to_csv(output_file)
except:
    print("The file %s does not exist!" % args.opf)


# example queries
df.loc[(df.chapter==1)&(df.verse==1)]
df.loc[(df.chapter==1)&(df.verse==2)]
df.loc[(df.chapter==1)&(df.verse==3)]

# example text retrieval
(df.head(8).token_prefix + df.head(8).token ).sum()
(df.head(8).token_prefix.fillna('') + df.head(8).token ).sum()