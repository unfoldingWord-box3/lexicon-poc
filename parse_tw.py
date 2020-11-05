import glob
import os
import re

import pandas as pd

files = glob.glob('./data/en_tw/bible/**/*.md', recursive=True)
data = {}
for f in files: 
    with open(f) as opf:
        filename = os.path.basename(f)
        subdir = f.split('/')[-2]  # names, kt, other
        identifier = filename.replace('.md', '')
        data[subdir + '/' + identifier] = opf.read()

output = []

for name,content in data.items():
    try:
        header = re.findall('^#.*?\n\n', content)[0].strip('#').strip()
    except:
        header = ''
    try: 
        definition = re.findall(r'## Definition:(.*?)##', content, re.DOTALL)[0].strip()
    except:
        definition = ''
    try:    
        suggestions = re.findall(r'## Translation Suggestions:(.*?)##', content, re.DOTALL)[0].strip()
    except:
        suggestions = ''
    try:
        refs = re.findall(r'## Bible References:(.*?)##', content, re.DOTALL)[0].strip()
    except:
        refs = ''
    try: 
        strongs = re.findall(r'## Word Data:(.*?)$', content, re.DOTALL)[0].strip()
    except:
        strongs = ''
    output.append({'name': name.split('/')[1],
                   'category': name.split('/')[0],
                   'header': header,
                   'definition': definition,
                   'suggestions': suggestions,
                   'refs': refs,
                   'strongs': strongs
    })

df = pd.DataFrame(output)
print(df)

df.to_csv('./data/alignment/tw.csv')

