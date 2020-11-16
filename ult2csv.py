import re
import pandas as pd
import argparse
import sys
import os

from parse_utils import parse_usfm

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


print('There are {} tokens in the document.'.format(len(contents.split())))

# Process the data 
words = parse_usfm(contents)
df_full = pd.DataFrame(words)
bookname = os.path.basename(input_file).replace('.usfm', '')
df_full = df_full.assign(book=[bookname]*df_full.shape[0])
try:
    df_full = df_full.assign(alg_id=df_full.book + "-" + df_full.alg_id.fillna('').astype(str))
except AttributeError:
    print('No alignment here')

try:
    os.path.exists(os.path.abspath(output_file))
    df_full.to_csv(output_file)
except:
    print("The file %s does not exist!" % args.opf)