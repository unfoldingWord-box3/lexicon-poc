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

For this PoC there are multiple options:
1. Create a state machine that parses token per token and keeps track of its embedding.
    Such a model is a lexer-parser type of model.
2. Parse the main building blocks such as the header, the chapters, and sections as these
are all relatively predictable. Then parse each chunk of text and extract the alignments.
Put these in a pandas dataframe and extract the data at token level.
3. Encode the data as a tree

I here opt for model 2. 

To find tags: set(re.findall(r'\\.*?\s', contents, re.DOTALL))
'''

import re


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


def parse_usfm(contents):
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
    return words