

'''
Description of the format of the data
=====================================

There are four categories of metadata: 

1. key-values such as `\ide UTF-8` and `\h 1 Kings`
2. Other items have opening and closing tags:
    \w ... \w*        # tag is repeated
    \zaln-s ... \*    # opened then the attributes follow, then closed
    \zaln-e\*         # opened and closed simultaneously
3. Some items are not surrounded by a tag, such as punctuation.
4. Some tags have no values: \s5 \p

Footnotes are in the following shape: \f + \ft Some versions have, \fqa the ark of Yahweh  \fqa* . \f* 
Whitespace is not meaningful.

Attributes are specified after a `|` in the format `attr="value"`. 
Attributes can be separated by spaces. 
In this set of USFM documents all attributes have `x-*` prepended.

The alignment data is structured following these principles

1. Linking: Embedding a target language word within a a zalg-start/zalg-end pair means 
    that the target language word is aligned with the source language word
2. Grouping: Nesting multiple source language words combines them in a group.
    Embedding multiple target language words groups them.
3. Gapping: To refer to words that have a gap one can refer to their x-occurrence. 
    If two alignments refer to the same source language occurrence, they form a single 
    alignment. This principle is implicit.
    
\\usfm either ends with a linebreak OR with another key_value tag
'''

import re
import pandas as pd

# with open('./data/en_ult/18-JOB.usfm') as ipf: 
# with open('./data/en_ult/01-GEN.usfm') as ipf: 
with open('./data/en_ult/29-JOL.usfm') as ipf: 
# with open('./data/alignment-example.usfm') as ipf: 
# with open('./data/en_ult/41-MAT.usfm') as ipf: 
# with open('./data/el-x-koine_ugnt/41-MAT.usfm') as ipf: 
    contents = ipf.read()

print('There are {} tokens in the sample.'.format(len(contents.split())))

set(re.findall(r'\\.*?\s', contents, re.DOTALL)) 

# These can be bound be a space or a newline, so really by the next tag
KEY_VALUE = [
 '\\c ',
 '\\id ',
 '\\ide ',
 '\\mt ',
 '\\toc1 ',
 '\\toc2 ',
 '\\toc3 ',
 '\\usfm ',
 '\\h ',
 '\\v ',
]

# these can be embedded
OPEN_CLOSING = [
 ('\\zaln-s', '\\*'),
 ('\\zaln-e', '\\*'),
 ('\\k-s', '\\*'),
 ('\\k-e', '\\*'),
 ('\\w ', '\\w* '),
 ('\\f ', '\\f* '),
 ('\\fqa ', '\\fqa* '), # Footnote translation quotation alternative
]

SWITCHES = [
 '\\p ',
 '\\s5 ',
 '\\q ',  # quotes end at the end of the sentence, this is implicit
 '\\q2 ',
 '\\ft ', # "essential (explanatory) text of the footnote", also implicitly closed
]

'''
Multiple options:
1. Create a state machine that parses token per token and keeps track of its embedding.
    Such a model is a lexer-parser type of model.
2. Parse the main building blocks such as the header, the chapters, and sections as these
are all relatively predictable. Then parse each chunk of text and extract the alignments.
Put these in a pandas dataframe and extract the data at token level.
3. Encode the data as a tree

I here opt for model 2. 
'''

chapters = contents.split('\c ')
header = chapters[0]
header = ' '.join(header.split())  # remove linebreaks because they are untrustworthy
chapters.pop(0)  # remove the header

HEADER = {}
for key in KEY_VALUE:
    # find the key and select everything until the next backslash
    value = re.findall(r'\{}[^\\]*'.format(key), header)
    # only select the first item of the resuls list
    try: 
        HEADER[key.strip().strip('\\')] = value[0].strip().lstrip(key)
    except IndexError:
        print(f'For {key} there is no value')
print(HEADER)

# parse the remainder of the chapters, 
# extract the words, and their alignment data
words = []
i = 1

for chapter in chapters:
    chapter_nr = re.findall(r'^\d+', chapter)[0]
    chapter = chapter.lstrip(chapter_nr).strip()
    
    # remove the switches
    for switch in SWITCHES:
        chapter = chapter.replace(switch, '')
        chapter = ' '.join(chapter.split())  # remove left-over linebreaks

    verses = chapter.split('\\v ')
    # remove the part before the first verse
    verses.pop(0)
    for verse in verses:
        verse_nr = re.findall(r'^\d+', verse)[0]
        verse = verse.lstrip(verse_nr).strip()
        verse = ' '.join(verse.split())  # remove left-over linebreaks
        if 'zaln-s' in verse:
            alignments = verse.split('\\zaln-e\\*')
            for alignment in alignments:
                align_data = re.findall(r'\\zaln-s.*?\*', alignment) 
                raw_word_data = re.sub(r'\\zaln-s.*?\*', '', alignment)
                for word in raw_word_data.split('\w*'): 
                    words.append({'token': word, 'alg': align_data, 'alg_id':i, 'chapter':chapter_nr, 'verse':verse_nr})
                i += 1
        elif '\w' in verse:
            raw_words = verse.split('\w*')
            for word in raw_words:
                words.append({'token': word, 'chapter':chapter_nr, 'verse':verse_nr})
        else: 
            raw_words = verse.split()
            for word in raw_words:
                words.append({'token': word, 'chapter':chapter_nr, 'verse':verse_nr})

# Process the data 
df_full = pd.DataFrame(words)
print(df_full)

## get source text phrases
source_blocks = df_full.groupby('alg_id').first()
source_blocks = source_blocks.explode('alg')  # do not ignore the index
source_blocks = source_blocks.assign(source_token=source_blocks.alg.str.extract(r'x-content=\"(.*?)\"'))
source_blocks_dict = source_blocks.groupby('alg_id').apply(lambda x: ' '.join(x.source_token.fillna(''))).to_dict()
df_full = df_full.assign(source_blocks=df_full.alg_id.map(source_blocks_dict))

# NB: discard the rows *without* alignment
df_full = df_full.loc[df_full.token != '',:]
print(df_full)

df = df_full.loc[df_full.alg.isnull()==False,:]
# df = df.loc[df.token != '',:]

# Change float to int 
df['alg_id'] = df['alg_id'].astype(int)

## There are cases where an alignment is interrupted
# find cases where the alignment id is different, 
# but the entire alignment group is the same
# the selected alignment id's should actually be given the same
# future versions of this script could include indicating a gap 
# The example that triggered this code is 
#   'as X reclined to eat' (cf. Mat 9:10)
# To retrieve it, use `df.loc[(df.chapter == '9') & (df.verse == '10')]`

df['sample_alg_str'] = df.alg.astype(str)
need_to_be_merged = df.groupby('chapter verse sample_alg_str'.split()).alg_id.unique()
need_to_be_merged = need_to_be_merged[need_to_be_merged.apply(len) > 1].tolist()

merging = {}
for itm in need_to_be_merged:
    for element in itm[1:]:
        # for each element refer to the first occurrence of the alignment
        merging[element] = itm[0]
# store the original alignment id
df['alg_id_old'] = df['alg_id']
# merge these alg_id to make them a single one
df.loc[df['alg_id'].isin(merging.keys()), 'alg_id'] = df['alg_id'].map(merging)

## There are cases with embedded alignment
df.loc[:, 'nrOfAlg'] = df.alg.fillna('').apply(len)
df.loc[df.nrOfAlg > 1]

# Extract the target data
df = df.assign(target_token=df.token.str.extract(r'\w( .*?)\|'))
df = df.assign(target_token_prefix=df.token.str.strip().str.extract(r'(.*?)(\\w)m( .*?)\|')[0])  # this selects the first group, viz. whatever occurs *before* \w
df = df.assign(target_occ=df.token.str.extract(r'x-occurrence=\"(.*?)\"'))
df = df.assign(target_occs=df.token.str.extract(r'x-occurrences=\"(.*?)\"'))

# Highlight a gap with … 
def find_gaps(li):
    pairs = list(zip(li, li[1:]))
    has_gap = []
    for idx,itm in enumerate(pairs):
        if itm[1] - itm[0] > 1:
            has_gap.append(idx)
    return [li[i] for i in has_gap]

have_gaps = df.loc[df.alg_id.isin(merging.values())].groupby('alg_id').apply(lambda x: find_gaps(x.index.tolist()))
need_gap_highlighting = [i for itm in have_gaps.tolist() for i in itm]
df.loc[:,'alg_has_gap'] = False
df.loc[need_gap_highlighting, 'alg_has_gap'] = True
df.to_excel('./data/alignment/target.xlsx')  # CAREFUL: this only exports THOSE TOKENS WITH AN ALIGNMENT
df.to_csv('./data/alignment/target.csv')  # CAREFUL: this only exports THOSE TOKENS WITH AN ALIGNMENT

# do this after so the export above is still clear
df.loc[df.alg_has_gap, 'target_token'] = df.loc[df.alg_has_gap, 'target_token'] + ' … '

# move each element in the `alg` array to a separate row
# ignore index avoids copying the index of a row that is exploded
df = df.explode('alg', ignore_index=True)

# Extract the source data
df = df.assign(strongs=df.alg.str.extract(r'x-strong=\"(.*?)\"'))
df = df.assign(lemma=df.alg.str.extract(r'x-lemma=\"(.*?)\"'))
df = df.assign(morph=df.alg.str.extract(r'x-morph=\"(.*?)\"'))
df = df.assign(source_token=df.alg.str.extract(r'x-content=\"(.*?)\"'))
df = df.assign(source_occ=df.token.str.extract(r'x-occurrence=\"(.*?)\"'))
df = df.assign(source_occs=df.token.str.extract(r'x-occurrences=\"(.*?)\"'))
df.loc[:, 'hasPrefix'] = False
df.loc[df.strongs.str.contains(r'd:|c:|l:|i:|k:|b:|m:').fillna(False), 'hasPrefix'] = True
df.loc[:, 'strongsNoPrefix'] = df.strongs.str.strip('d:|c:|l:|i:|k:|b:|m:')

df.to_excel('./data/alignment/alignment.xlsx')
df.to_csv('./data/alignment/alignment.csv')

# Do some analysis


# phrase alignments
target_tokens = df.groupby('strongs alg_id'.split()).apply(lambda x: x.target_token.fillna('').sum())
target_tokens.shape
# get the lemma
lemmata = df.groupby('strongs alg_id'.split()).lemma.first()
source_tokens = df.groupby('strongs alg_id'.split()).source_token.first()
source_blocks = df.groupby('strongs alg_id'.split()).source_blocks.first()

allinone = pd.concat([target_tokens, lemmata, source_tokens, source_blocks], axis=1)
allinone.rename(columns={0:'target_blocks'}, inplace=True)
dense = allinone.groupby('strongs target_blocks'.split()).size()
dense
allinone.groupby('strongs target_blocks'.split()).size()
allinone.groupby('strongs source_blocks target_blocks'.split()).size().head(60)

allinone.to_csv('./data/alignment/dictionary.csv')
allinone.to_excel('./data/alignment/dictionary.xlsx')

# get the counts for each sense
counts = allinone.groupby(['strongs', 'target_blocks']).size()
counts.to_excel('./data/alignment/counts.xlsx')
counts.to_csv('./data/alignment/counts.csv')
counts.head(50)

# query a strongs number
allinone.loc['G00180']

# find synonyms
allinone.loc[allinone['target_blocks'].str.contains('bad')]
allinone.loc[allinone['target_blocks'].str.contains('said')].lemma.value_counts()

# IDEA
# if a word is aligned with many different strongs numbers, surely it is a function word
# I could doc frequency to identify these function words

# alternatively
# you could re-align these using a pre-trained aligner? 
# or you could start with cases without any prefixes
df.loc[df.alg.str.get(0).fillna('').str.contains('c:H0559')].target_token.str.upper().value_counts()

# how do you group the entries into senses?

# more query examples
kings = df.loc[df.alg.fillna('').str.contains('H4428')]
kings.source_token.str.upper().value_counts()
kings.target_token.str.upper().value_counts()

# for אֵת this does not work
df.loc[df.alg.str.get(0).fillna('').str.contains('H0853')].target_token.str.upper().value_counts()

# son / sons , my/your/his/a
df.loc[df.alg.str.get(0).fillna('').str.contains('H1121a')].target_token.str.upper().value_counts()

df.loc[df.strongsNoPrefix == 'H0559'].target_token.str.upper().value_counts()
df.loc[-df.hasPrefix]

# IDEAS
# we are going to find a lot of alignment mistakes, maybe even translation mistakes
# ideally we could develop a memory-based or a dictionary-based alignment
# can I create a tool that automatically
# 1. uses synonyms to make a translation more dynamic
# 2. a webapp that reads ufsm files and transforms them to tsv


# compare the frequencies to find the headwords
# compare the document frequency

# get the metaphorical usages based on translationWords or figs-