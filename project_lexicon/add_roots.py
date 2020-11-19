import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_lexicon.settings")
django.setup()

import spacy
import pandas as pd

from lexicon.models import Alignment

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
    algs = Alignment.objects.filter(target_blocks=target_block)
    algs.update(roots=root)

# roots = []
# for itm in allinone.target_blocks.tolist():
#     parsing = parse(itm)
#     # print()
#     # print(parsing.loc[parsing.dep == 'ROOT', 'lemma'].tolist(), itm)
#     roots.append(parsing.loc[parsing.dep == 'ROOT', 'lemma'].tolist()[0])
# allinone['roots'] = roots




# # phrase alignments
# target_tokens = df.groupby('strongs alg_id'.split()).apply(lambda x: x.target_token.fillna('').sum())
# target_tokens.shape
# # get the lemma
# lemmata = df.groupby('strongs alg_id'.split()).lemma.first()
# source_tokens = df.groupby('strongs alg_id'.split()).source_token.first()
# source_blocks = df.groupby('strongs alg_id'.split()).source_blocks.first()

# allinone = pd.concat([target_tokens, lemmata, source_tokens, source_blocks], axis=1)
# allinone.rename(columns={0:'target_blocks'}, inplace=True)

# # choose a root for each alignment
# nlp = spacy.load("en_core_web_sm")

# def parse(input_string):
#     output = []
#     doc = nlp(input_string)
#     for token in doc:
#         output.append([token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#                 token.shape_, token.is_alpha, token.is_stop])
#     return pd.DataFrame(output, columns='token lemma pos tag dep shape is_alpha is_stop'.split())

# roots = []
# for itm in allinone.target_blocks.tolist():
#     parsing = parse(itm)
#     # print()
#     # print(parsing.loc[parsing.dep == 'ROOT', 'lemma'].tolist(), itm)
#     roots.append(parsing.loc[parsing.dep == 'ROOT', 'lemma'].tolist()[0])
# allinone['roots'] = roots

# dense = allinone.groupby('strongs target_blocks'.split()).size()
# dense
# allinone.groupby('strongs target_blocks'.split()).size()
# allinone.groupby('strongs source_blocks target_blocks'.split()).size().head(60)

# allinone.to_csv('./data/alignment/dictionary.csv')
# ## allinone.to_excel('./data/alignment/dictionary.xlsx')

# # get the counts for each sense
# counts = allinone.groupby(['strongs', 'target_blocks']).size()
# ## counts.to_excel('./data/alignment/counts.xlsx')
# counts.to_csv('./data/alignment/counts.csv')
# counts.head(50)

# # EXPORT
# # the target/gateway language

# df.loc[-df.token.isnull(), ['Unnamed: 0', 'orig_id', 'token', 'chapter', 'verse',
#        'book', 'alg_id', 'target_token', 'target_token_prefix',
#        'target_occ', 'target_occs']].reset_index(drop=True)
# #FIXME wrong alignment id's
# df.loc[df.alg_id=='06-JOS200']
# df.alg_id.value_counts()


# # query a strongs number
# allinone.loc['G00180']

# # find synonyms
# allinone.loc[allinone['target_blocks'].str.contains('bad')]
# allinone.loc[allinone['target_blocks'].str.contains('said')].lemma.value_counts()

# # IDEA
# # if a word is aligned with many different strongs numbers, surely it is a function word
# # I could doc frequency to identify these function words

# # alternatively
# # you could re-align these using a pre-trained aligner? 
# # or you could start with cases without any prefixes
# df.loc[df.alg.str.get(0).fillna('').str.contains('c:H0559')].target_token.str.upper().value_counts()

# # how do you group the entries into senses?

# # more query examples
# kings = df.loc[df.alg.fillna('').str.contains('H4428')]
# kings.source_token.str.upper().value_counts()
# kings.target_token.str.upper().value_counts()

# # for אֵת this does not work
# df.loc[df.alg.str.get(0).fillna('').str.contains('H0853')].target_token.str.upper().value_counts()

# # son / sons , my/your/his/a
# df.loc[df.alg.str.get(0).fillna('').str.contains('H1121a')].target_token.str.upper().value_counts()

# df.loc[df.strongsNoPrefix == 'H0559'].target_token.str.upper().value_counts()
# df.loc[-df.hasPrefix]





# # IDEAS
# # we are going to find a lot of alignment mistakes, maybe even translation mistakes
# # ideally we could develop a memory-based or a dictionary-based alignment
# # can I create a tool that automatically
# # 1. uses synonyms to make a translation more dynamic
# # 2. a webapp that reads ufsm files and transforms them to tsv


# # compare the frequencies to find the headwords
# # compare the document frequency

# # get the metaphorical usages based on translationWords or figs-