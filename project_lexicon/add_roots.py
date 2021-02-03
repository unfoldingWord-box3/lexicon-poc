import os, django
import spacy
import pandas as pd
from sqlalchemy import create_engine


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_lexicon.settings")
django.setup()

from lexicon.models import Alignment

engine = create_engine('sqlite:///../project_lexicon/alignment.db', echo=False)
engine.execute('ALTER TABLE %s ADD COLUMN %s %s' % ('alignment', 'roots', 'TEXT'))

alignments = Alignment.objects.filter(roots__isnull=True).values_list('target_blocks').distinct()  # [:10]

# # choose a root for each alignment

nlp = spacy.load("en_core_web_sm")

def parse(input_string):
    output = []
    doc = nlp(input_string)
    for token in doc:
        output.append([token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                token.shape_, token.is_alpha, token.is_stop])
    return pd.DataFrame(output, columns='token lemma pos tag dep shape is_alpha is_stop'.split())

to_store = {}

for itm in alignments:
    itm = itm[0]
    parsing = parse(itm)
    print(itm)
    to_store[itm] = parsing.loc[parsing.dep == 'ROOT', 'lemma'].tolist()[0]

for target_block,root in to_store.items():
    print('storing', target_block, root)
    algs = Alignment.objects.filter(target_blocks=target_block)
    algs.update(roots=root)
