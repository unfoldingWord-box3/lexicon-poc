import glob
import os
import re
from itertools import permutations
import pandas as pd

from engine import engine

files = glob.glob('../data/en_tw/bible/**/*.md', recursive=True)
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
df['id'] = df.index.tolist()
print(df)

# link these notes to the Source table
source = pd.read_csv('../data/csv/source.csv')
source.drop('Unnamed: 0', axis=1, inplace=True)

# extract both category and name
cat_and_name = source.translation_word.str.extract(r'.*?bible\/(.*?)\/(.*)')
source['category'] = cat_and_name[0]
source['name'] = cat_and_name[1]
source = source.merge(df[['id', 'category', 'name']], on=['category', 'name'], how='left')
source = source.rename(columns={'id_y':'tw_id', 'id_x':'id'})

# create a Strongs table that is a m2m to itself,
# this might be a bit overkill (linking from a->b and from b->a)
strongs = pd.DataFrame(source.strongs_no_prefix.value_counts().index.sort_values(), columns=['number'])
strongs['id'] = strongs.index.tolist()
raw_strongs = df.strongs.str.extract(r'\* Strong’s\: (.*)')[0]
to_add_to_m2m = raw_strongs.str.split(', ')
m2m = []
for row in to_add_to_m2m.reset_index().itertuples():
    try:
        for itm in permutations(row[2], 2):
            m2m.append(itm)
    except:
        print('Does not have strongs')
#TODO in the future we can link this strongs table to the Source table and denormalize
strongs_m2m = pd.DataFrame(m2m, columns=['number', 'related_number'])

df.to_csv('../data/csv/words.csv')
source.to_csv('../data/csv/source.csv')
strongs_m2m.to_csv('../data/csv/strongs_m2m.csv')

source.to_sql('source', con=engine, if_exists='replace')
df.to_sql('tw', con=engine, if_exists='replace')
strongs_m2m.to_sql('strongs_m2m', con=engine, if_exists='replace')