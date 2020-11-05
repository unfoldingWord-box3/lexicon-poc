import re
import pandas as pd

with open('./data/el-x-koine_ugnt/41-MAT.usfm') as ipf: 
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
df_full.rename(columns={'token': 'source_token'}, inplace=True)

df = df_full.loc[df_full.source_token != '',:]
print(df)

# Extract the target data
df = df.assign(token=df.source_token.str.extract(r'\w( .*?)\|'))
df = df.assign(token_prefix=df.source_token.str.strip().str.extract(r'(.*?)(\\w)( .*?)\|')[0])  # this selects the first group, viz. whatever occurs *before* \w
df = df.assign(morph=df.source_token.str.extract(r'x-morph=\"(.*?)\"'))
df = df.assign(lemma=df.source_token.str.extract(r'lemma=\"(.*?)\"'))
df = df.assign(strongs=df.source_token.str.extract(r'strong=\"(.*?)\"'))
df = df.assign(translation_word=df.source_token.str.extract(r'x-tw=\"(.*?)\"'))

print(df)
# df = df.assign(target_occ=df.token.str.extract(r'x-occurrence=\"(.*?)\"'))
# df = df.assign(target_occs=df.token.str.extract(r'x-occurrences=\"(.*?)\"'))
df.to_excel('./data/alignment/source.xlsx')
