import glob
import subprocess
import os

input_files = glob.glob('../../../data/en_tn-v34/en_tn/*.tsv')

for ipf in input_files:
    basename = os.path.basename(ipf)
    with open(basename.replace('.tsv', 'Parsed.tsv'), "w") as opf:
        print('Processing', ipf)
        subprocess.call(['node', 'tn4lexicon.js', ipf], stdout=opf)
        print('Finished processing', ipf)
        print()