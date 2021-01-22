import glob
import re
import os
from itertools import chain
from sqlalchemy import create_engine
import numpy
import pandas as pd

# Read and transform the markdown files
hebrew_files = glob.glob('./data/en_uhal/content/*.md')
greek_files = glob.glob('./data/en_ugl/content/**/*.md')
files = hebrew_files + greek_files

data = {}
for f in files: 
    if 'index' in f:
        continue
    with open(f) as ipf:
        # this will not work for the three stray md files that are not nested in a directory
        # life's a thug
        if 'ugl' in f:            
            filename = f.split('/')[-2:-1][0]
            identifier = filename.strip('.md')
        else:
            filename = os.path.basename(f)
            identifier = filename.strip('.md')
        data[identifier] = { 'raw':ipf.read().strip()}

print(f'There are {len(data)} files')

# Study the data structures
sample = list(data.keys())[12500]  # use 1250 and 12500 as samples
sample = data[sample]['raw']
headings = re.findall('#.*?\n\n', sample)

# What follows assumes that the markdown files contain structured data (the order of the data is important)
def clean(text):
    return text.strip(': \n')

lemma = re.findall(r'^# (.*?)\s+', sample, re.DOTALL)[0]
lemma = clean(lemma)
meta = re.findall(r'<!--(.*?)-->', sample, re.DOTALL)
meta = '\n'.join([clean(itm) for itm in meta])
word_data = re.findall(r'Word data(.*?)##', sample, re.DOTALL)[0]
word_data = clean(word_data)
etymology = re.findall(r'Etymology(.*?)##', sample, re.DOTALL)[0]
etymology = clean(etymology)
senses = re.findall(r'Senses(.*?)$', sample, re.DOTALL)[0]
senses = clean(senses)
split_senses = re.split('\s###\s', senses, re.DOTALL)
split_senses = [clean(itm) for itm in split_senses]

headings = ['#### Definition', '#### Glosses', '#### Explanation', '#### Citations']

sense_output = {}
for sense in split_senses:
    # I end the str with a # so that a single regex can go all the way to the end
    sense = sense + '#'
    sense_header = re.findall(r'Sense(.*?)#', sense, re.DOTALL)[0]
    sense_data_for_output = {}
    for heading in headings: 
        
        tmp = re.findall(r'{}(.*?)#'.format(heading), sense, re.DOTALL)[0]
        tmp = clean(tmp)
        sense_data_for_output[heading.strip('# \n:')] = tmp

    sense_output[sense_header.strip('# \n:')] = sense_data_for_output


ERRORS = ['G35830',  # uses wrong level for sense description
          'G48040',  # mistake in Sense header (adds .)
          'G39720',  # fails to define first sense
         ]

lexicon = {}
headings = ['#### Definition', '#### Glosses', '#### Explanation', '#### Citations']


for key,val in data.items():
    if key in ERRORS:
        continue 
        
    output = {}

    
    # I end the file with a # so that a single regex can go all the way to the end
    # without shenanigans for the citations at the end of the file
    raw_text = val['raw'] + '#'
    
    # some of the Greek entries have internal references in the form of
    # (sense-10)
    # these anchors hamper the text extraction and hence I replace the # character
    # on the assumption that the - indicates that it is not a heading
    raw_text = raw_text.replace('#sense-', '->sense-')
    # ah, more human errors, great
    raw_text = raw_text.replace('#sense–', '->sense-')
    
    try: 
        # certain Greek entries miss the lemma / header
        lemma = re.findall(r'^# (.*?)\s+', raw_text, re.DOTALL)[0]
        lemma = clean(lemma)
    except:
        lemma = None
    try:
        meta = re.findall(r'<!--(.*?)-->', raw_text, re.DOTALL)
        meta = '\n'.join([clean(itm) for itm in meta])
    except:
        meta = None
    try:
        word_data = re.findall(r'Word data(.*?)##', raw_text, re.DOTALL)[0]
        word_data = clean(word_data)
    except:
        word_data = None
    etymology = re.findall(r'Etymology(.*?)##', raw_text, re.DOTALL)[0]
    etymology = clean(etymology)
    senses = re.findall(r'Senses(.*?)$', raw_text, re.DOTALL)[0]
    senses = clean(senses)
    split_senses = re.split(r'\s###\s', senses, re.DOTALL)
    split_senses = [clean(itm) for itm in split_senses]

    headings = ['#### Definition', '#### Glosses', '#### Explanation', '#### Citations']

    sense_output = {}
    for sense in split_senses:
        # I end the str with a # so that a single regex can go all the way to the end
        sense = sense + '#'
        sense_header = re.findall(r'Sense(.*?)#', sense, re.DOTALL)[0]
        sense_data_for_output = {}
        for heading in headings: 

            try:
                tmp = re.findall(r'{}(.*?)#'.format(heading), sense, re.DOTALL)[0]
                tmp = clean(tmp)
            except:
                tmp = None
            sense_data_for_output[heading.strip('# \n:')] = tmp

        sense_output[sense_header.strip('# \n:')] = sense_data_for_output
  
    output['lemma'] = lemma
    output['meta'] = meta
    output['word_data'] = word_data
    output['etymology'] = etymology
    output['senses'] = sense_output
   
    lexicon[key] = output

len(data) - len(lexicon)

lexdf = pd.DataFrame(lexicon).T

lexdf['status'] = lexdf.meta.fillna('').str.findall(r'Status(.*?)\n').str.get(0).str.strip('\s.:')
lexdf['lexica_used'] = lexdf.meta.fillna('').str.findall(r'\n(.*?)$').str.get(0).str.strip('\s.:')
lexdf['parsed_strongs'] = lexdf.word_data.str.findall(r'\* Strongs:(.*?)\n').str.get(0).str.strip('\s.')
lexdf['TWOT'] = lexdf.word_data.str.findall(r'TWOT:(.*?)\n').str.get(0).str.strip('\s.')
lexdf['BDB'] = lexdf.word_data.fillna('').str.findall(r'BDB(.*?)\n').str.get(0).fillna('').str.strip('\s.')
lexdf['LXX'] = lexdf.etymology.fillna('').str.findall(r'LXX/Hebrew glosses(.*?)Time Period', flags=re.DOTALL).str.get(0).fillna('').str.strip('\s.:\n')
lexdf['LXX'] = lexdf['LXX'].str.strip('\*\n\s ')
lexdf['nr_of_senses'] = lexdf.senses.apply(len)
lexdf['strongs'] = lexdf.index.tolist()

lexdf['senses'] = lexdf['senses'].astype(str)

lexdf.to_csv('./data/lexicon.csv')

engine = create_engine('sqlite:///project_lexicon/alignment.db', echo=False)
lexdf.to_sql('lexicon', con=engine, if_exists='replace')