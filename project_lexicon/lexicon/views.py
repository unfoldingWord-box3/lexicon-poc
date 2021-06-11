import json
import random
from collections import OrderedDict, Counter
from itertools import groupby
import copy
import pandas as pd

from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import (BDB_senses, Source, 
    Target, Alignment, StrongsM2M, 
    Notes, Words, Collocations,
    BDB_strongs, BDB, Dodson
)


# UTILS 

HEBREW_ACCENTS = '''
    \u0591
    \u0592
    \u0593
    \u0594
    \u0595
    \u0596
    \u0597
    \u0598
    \u0599
    \u0592
    \u059A
    \u059B
    \u059C
    \u059D
    \u059E
    \u059F
    \u05A0
    \u05A1
    \u05A2
    \u05A3
    \u05A4
    \u05A5
    \u05A6
    \u05A7
    \u05A8
    \u05A9
    \u05AA
    \u05AB
    \u05AC
    \u05AD
    \u05AE
    \u05AF
    '''.split()


HEBREW_VOWELS = '''
    \u05B0
    \u05B1
    \u05B2
    \u05B3
    \u05B4
    \u05B5
    \u05B6
    \u05B7
    \u05B8
    \u05B9
    \u05BA
    \u05BB
    \u05C7
    '''.split()

HEBREW_PUNKT = '''
    \u05BC
    \u05BD
    \u05BF
    \u05C0
    \u05C3
    \u05C4
    \u05C5
    \u05C6
    \u05EF
    \u05F3
    \u05F4
    '''.split()

HEBREW_MAQEF = '''
    \u05BE
    '''.split()

HEBREW_SIN_SHIN_DOTS = '''
    \u05C1
    \u05C2
        '''.split()

HEBREW_CONSONANTS = '''
    \u05D0
    \u05D1
    \u05D2
    \u05D4
    \u05D5
    \u05D6
    \u05D7
    \u05D8
    \u05D9
    \u05DA
    \u05DB
    \u05DC
    \u05DD
    \u05DE
    \u05DF
    \u05E0
    \u05E1
    \u05E2
    \u05E3
    \u05E4
    \u05E5
    \u05E6
    \u05E7
    \u05E8
    \u05E9
    \u05EA
    '''.split()

HEBREW_WITH_DAGESH_OR_DOT = '''
    \uFB2A
    \uFB2B
    \uFB2C
    \uFB2D
    \uFB2E
    \uFB32
    \uFB2F
    \uFB30
    \uFB31
    \uFB33
    \uFB34
    \uFB35
    \uFB36
    \uFB37
    \uFB38
    \uFB39
    \uFB3A
    \uFB3B
    \uFB3C
    \uFB3D
    \uFB3E
    \uFB3F
    \uFB40
    \uFB41
    \uFB42
    \uFB43
    \uFB44
    \uFB45
    \uFB46
    \uFB47
    \uFB48
    \uFB49
    '''.split()


HEBREW_ADVANCED = '''
    \uFB1D
    \uFB1E
    \uFB1F
    \uFB20
    \uFB21
    \uFB22
    \uFB23
    \uFB24
    \uFB25
    \uFB26
    \uFB27
    \uFB28
    \uFB29
    \uFB4A
    \uFB4B
    \uFB4C
    \uFB4D
    \uFB4E
    \uFB4F
    '''.split()


COLOR_SCALE = {1:'darken-4',
           2:'darken-3',
           3:'darken-2',
           4:'lighten-1',
           5:'lighten-2',
           6:'lighten-3',
           7:'lighten-4',
           8:'lighten-5',
           9:'lighten-5',
           10:'lighten-5',
}
for i in range(11,5000): COLOR_SCALE[i] = 'lighten-5'

ICON_SCALE = {
    1:'looks_one',
    2:'looks_two',
    3:'looks_3',
    4:'looks_4',
    5:'looks_5',
    6:'looks_6' }
for i in range(7,5000): ICON_SCALE[i] = ''


def get_font(entry_id):
    if entry_id[0]=='A': 
        font='hb'
    elif entry_id[0]=='H': 
        font='hb'
    elif entry_id[0]=='G': 
        font='gk'
    else:
        font=None
    return font


def expand_window(li, window=5):
    '''
    >>> expand_window([20])
    {15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25}

    >>> expand_window([20])
    {15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25}
    '''
    output = []
    for itm in li:
        for i in range(-window,window+1):
            output.append(itm+i)
    return set(output)


def build_concordance(token_ids, window_tokens, highlights=[], window=5):
    '''
    >>> build_concordance([1,2], {1:'In', 2:'the', 3:'beginning'})
    ['<span class="hl">In</span>', '<span class="hl">the</span>', 'beginning']

    >>> build_concordance([1,2], {1:'In', 2:'the', 3:'beginning'}, highlights=[3])
    ['<span class="hl">In</span>',
    '<span class="hl">the</span>',
    '<span class="hl">beginning</span>']
    '''

    concordance = []  

    for i in range(min(token_ids)-window, max(token_ids)+window+1):
        try:
            token = window_tokens[i]
            if i in token_ids or i in highlights:
                token = '<span id="' + str(i) + '" class="hl">' + token + '</span>'
            if token:  # some cases are None
                concordance.append(token)
        except:
            continue
    return concordance


def remove_accents(input_string):
    for char in HEBREW_ACCENTS:
        input_string = input_string.replace(char, '')
    return input_string
    

# VIEWS 

def discovery(request):
    '''
    Fake some vertical data
    '''
    pass


def verticalize(request):
    '''
    Add a vertical annotation
    '''
    pass


def view_forms(request, entry_id):
    '''
    The current solution is suboptimal. What is needed instead is an SQL
    query that gets the frequency of each morph+token combination
    as well as a list of its alignments.
    '''
    source = Source.objects.filter(strongs_no_prefix=entry_id).prefetch_related('target_set')
    lemma = source[0].lemma
    font = get_font(entry_id)
    # alternative: /api/source/?book=&chapter=&verse=&strongs_no_prefix=&lemma=%D7%99%D6%B8%D7%9C%D6%B7%D7%93&token=&query={token,alignments{target_blocks}}
    # forms = source.values('morph', 'token').annotate(frequency=Count(['morph'])).order_by('-frequency')
    forms = set(source.values_list('id', 'morph', 'token', 'alignment__target_blocks'))

    # Create a form because namedtuples are immutable
    class Form():
        def __init__(self, id, morph, token, alg):
            self.id = id
            self.morph = morph
            self.token = token
            self.alg = alg

    forms = [Form(*itm) for itm in forms]
    # change the formatting per instance
    for row in forms:
        try:
            row.alg = row.alg.strip()
        except:
            pass
        row.token = remove_accents(row.token.strip())
    
    # compute the frequencies
    frequencies = Counter((row.morph, row.token) for row in forms)
    # add the alignments
    output = {}
    for itm,freq in frequencies.items():
        morph, token = itm
        algs = []
        for row in forms:
            if row.morph == morph and row.token == token and row.alg:
                algs.append(row.alg)
        output[(morph, token)] = (freq, ', '.join(set(algs)))
    # sort the output
    output = sorted(output.items(), key=lambda item: item[1], reverse=True)

    return render(request, 'lexicon/view_forms.html', {'lemma':lemma,
                                                       'entry':entry_id,
                                                       'forms':output,
                                                       'font':font,
                                                    #    'target_blocks':target_blocks,
                                                       })


def view_resources(request, entry_id):
    source = Source.objects.filter(strongs_no_prefix=entry_id)
    lemma = source[0].lemma
    words_ids = source.filter(words__isnull=False).distinct().values('words__id')
    words = Words.objects.filter(pk__in=words_ids)
    related_words = StrongsM2M.objects.filter(number=entry_id).values_list('related_number')
    strongs = Source.objects.filter(strongs_no_prefix__in=related_words).values_list('strongs_no_prefix', 'lemma').distinct()
    related_words = dict(strongs)
    # prefetch related is essential to keep the number of queries small
    notes = Notes.objects.filter(source__strongs_no_prefix=entry_id).prefetch_related('source', 'source__target_set')
    font = get_font(entry_id)

    return render(request, 'lexicon/view_resources.html', {'lemma':lemma,
                                                            'words':words,
                                                            'related_words':related_words,
                                                            'notes':notes,
                                                            'font':font,
                                                            'entry':entry_id})   


def view_dictionary(request, entry_id):
    lemma = Source.objects.filter(strongs_no_prefix=entry_id)[0].lemma
    font = get_font(entry_id)
    if entry_id.startswith('H'):
        bdb_entries_ids = BDB_strongs.objects.filter(strongs=entry_id).values('bdb')
        bdb_entries = BDB.objects.filter(bdb__in=bdb_entries_ids)
        return render(request, 'lexicon/view_dictionary.html', {'bdb_entries': bdb_entries, 
                                                            'entry':entry_id, 
                                                            'lemma':lemma,
                                                            'font':font,})
    if entry_id.startswith('G'):
        dodson = Dodson.objects.filter(strongs=entry_id)
        return render(request, 'lexicon/view_dictionary.html', {'dodson': dodson, 
                                                            'entry':entry_id, 
                                                            'lemma':lemma,
                                                            'font':font,})


def view_parsed_dictionary(request, entry_id):
    lemma = Source.objects.filter(strongs_no_prefix=entry_id)[0].lemma
    font = 'hb'
    if entry_id.startswith('H'):
        bdb_entries_ids = BDB_strongs.objects.filter(strongs=entry_id).values('bdb')
        bdb_entries = BDB.objects.filter(bdb__in=bdb_entries_ids).prefetch_related('bdbsensetosource_set', 'bdbsensetosource_set__source')
    else: 
        bdb_entries = ''
    return render(request, 'lexicon/view_parsed_dictionary.html', {'bdb_entries': bdb_entries, 
                                                            'entry':entry_id, 
                                                            'lemma':lemma,
                                                            'font':font,})



def view_collocates(request, lemma):
    try:
        node = Collocations.objects.get(node=lemma)
        lemma = node.node
        collocates = json.loads(node.context.replace("'", '"'))
    except ObjectDoesNotExist:
        node = ''   
        collocates = ''
    entry = Source.objects.filter(lemma=lemma).first().strongs_no_prefix
    font = get_font(entry)
    return render(request, 'lexicon/view_collocates.html', {'node':node, 
                                                            'collocates': collocates, 
                                                            'lemma':lemma,
                                                            'font':font,
                                                            'entry':entry,})


def view_cooccurrences(request, main_entry, sec_entry):
    '''
    Search for a strongs number AND another strongs number in its immediate vicinity

    ? when do you link to the alignment data?
    This is only the SOURCE, not the TARGET just yet.
    '''
    # main =  Source.objects.filter(strongs_no_prefix=main_entry)

    def clean(input_string):
        return input_string.replace('_', ' ')

    main =  Source.objects.filter(lemma=clean(main_entry))
    main_ids = [i[0] for i in main.values_list('id')]
    main_w_context = expand_window(main_ids)
    
    # secondary =  Source.objects.filter(strongs_no_prefix=sec_entry)
    secondary =  Source.objects.filter(lemma=clean(sec_entry))
    sec_ids = [i[0] for i in secondary.values_list('id')]
    sec_w_context = expand_window(sec_ids)

    main_window_tokens = dict(Source.objects.filter(id__in=main_w_context).annotate(full_token=Concat('token_prefix','token')).values_list('id', 'full_token'))

    highlights = []
    for word in sec_ids:
        if word in main_w_context: 
            highlights.append(word)

    lines = []

    for word in main_ids:
        if word in sec_w_context: 
            lines.append([word])

    output = []

    for line in lines:
        output.append(''.join(build_concordance(line, main_window_tokens, highlights=highlights)))
    
    return JsonResponse(output, safe=False)


def demo_entry(request):
    return render(request, 'lexicon/demo_entry.html')



def view_occurrences(request, entry_id):
    try:
        lemma = Source.objects.filter(strongs_no_prefix=entry_id)[0].lemma
    except:
        lemma = None
    font = get_font(entry_id)
    tokens = Source.objects.filter(strongs_no_prefix=entry_id)
    return render(request, 'lexicon/view_occurrences.html', {
        'entry':entry_id,
        'lemma': lemma,
        'font': font,
        'tokens': tokens,
        })


def view_entry(request, entry_id):
    try:
        lemma = Source.objects.filter(strongs_no_prefix=entry_id)[0].lemma
    except:
        lemma = None
    font = get_font(entry_id)

    result = Alignment.objects.filter(source__strongs_no_prefix=entry_id).values('id', 'alg_id', 'source__book', 'source__chapter', 'source__verse', 'source', 'source__token', 'source__morph', 'target', 'target__target_token', 'roots', 'source_blocks', 'target_blocks')

    source_ids = [itm['source'] for itm in result]
    source_ids_w_window = expand_window(source_ids)
    source_window_tokens = dict(Source.objects.filter(id__in=source_ids_w_window).annotate(full_token=Concat('token_prefix','token')).values_list('id', 'full_token'))

    target_ids = [itm['target'] for itm in result]
    target_ids_w_window = expand_window(target_ids)
    target_window_tokens = dict(Target.objects.filter(id__in=target_ids_w_window).annotate(full_token=Concat('target_token_prefix','target_token')).values_list('id', 'full_token'))

    # goal: alg_id, source_id, source_blocks, [target_id1, target_id2], [target_blocks1, target_blocks2], source_concordance, target_concordance
    # this assumes only a single source_id, even if multiple source words are part of the alignment
    # this is 'condensed' result as it merges multiple [target_ids, ...] into single lists
    condensed_result = []

    for idx,grp in groupby(result, lambda datum: datum['alg_id']):
        output = {}
        output['alg_id'] = idx

        for idx,itm in enumerate(grp):
            if idx == 0:
                # for the first item we do some extra's
                output['id'] = itm['id']
                output['alg_id'] = itm['alg_id']
                #TODO add the reference
                output['book'] = itm['source__book']
                output['chapter'] = itm['source__chapter']
                output['verse'] = itm['source__verse']
                output['source'] = [itm['source']]  # list because build_concordance needs a list
                output['source_blocks'] = itm['source_blocks']
                output['source__morph'] = itm['source__morph']
                output['target'] = [itm['target']]
                output['target__target_token'] = [itm['target__target_token']] # list
                output['target_blocks'] = itm['target_blocks']
                output['roots'] = itm['roots']
            else:
                output['target'] = output['target'] + [itm['target']] # list
                output['target__target_token'] = output['target__target_token'] + [itm['target__target_token']] # list
        condensed_result.append(output)

    # now add concordances
    algs_w_concordances = []
    for itm in condensed_result:
        itm['source_concordance'] = ''.join(build_concordance(itm['source'], source_window_tokens, window=4))
        itm['target_concordance'] = ''.join(build_concordance(itm['target'], target_window_tokens, window=8))
        algs_w_concordances.append(itm)

    # quickfix to start working with the data
    df = pd.DataFrame(algs_w_concordances)

    if request.GET.get('table'):
        table = df.to_html()
        return render(request, 'lexicon/view_entry_table.html', {
            'table':table,
            'entry':entry_id,
            'lemma': lemma,
            'font': font,
            })

    # start splitting out the senses
    COLUMN = 'target_blocks'
    if request.GET.get('roots'):
        COLUMN = 'roots'
    
    # now regroup per sense
    frequencies = df.drop_duplicates('alg_id').groupby(COLUMN).size().sort_values(ascending=False)
    # print(frequencies)
    senses_text = df.groupby(COLUMN).size().sort_values(ascending=False).index.tolist()
    senses = []
    for idx,freq in enumerate(frequencies.items(), start=1):
        # order, color, icon, frequency, 5 samples      
        sense, frequency = freq[0].strip(), freq[1]

        alg = df.loc[df[COLUMN]==freq[0]]
        if alg.shape[0] > 5:
            alg = alg.sample(5)

        senses.append({'freq': frequency,
                       'sense': sense,
                       'color': COLOR_SCALE[idx],
                       'order': idx,
                       'icon': ICON_SCALE[idx],
                       'source_samples': alg.source_concordance,
                       'target_samples': alg.target_concordance,
        })

    # tw_related_items = StrongsM2M.objects.filter(number=entry_id).values_list('related_number')
    # strongs = Source.objects.filter(strongs_no_prefix__in=tw_related_items).values_list('strongs_no_prefix', 'lemma').distinct()
    # tw_related_items = dict(strongs)
    
    # target_blocks = frequencies.index.tolist()
    # # .values('lemma', 'strongs')
    # if COLUMN == 'roots':
    #     sense_related_items = Alignment.objects.filter(roots__in=target_blocks).select_related('source').distinct()
    # else:
    #     sense_related_items = Alignment.objects.filter(target_blocks__in=target_blocks).select_related('source').distinct()
    # sense_dict = {}
    # for itm in sense_related_items:
    #     sense_dict[itm.source.strongs_no_prefix] = itm.source.lemma

    tw_related_items = {}
    sense_dict = {}
    
    sense_word_list = []
    for sense in senses:
        sense_word_list.extend(sense['sense'].upper().split())
    sense_word_list = list(set([itm for itm in sense_word_list if not itm == "…"]))

    # prefetch related is essential to keep the number of queries small
    notes = Notes.objects.filter(source__strongs_no_prefix=entry_id).prefetch_related('source', 'source__target_set')

    return render(request, 'lexicon/view_entry.html', {'senses':senses,
        'senses_text':senses_text,
        'entry':entry_id,
        'lemma': lemma,
        'font': font,
        'tw_related_items': tw_related_items,
        'sense_related_items': sense_dict,
        'sense_word_list':sense_word_list,
        'notes': notes,
        })


def view_entry_alignment(request, entry_id):
    lexicon = pd.read_csv('../data/csv/dictionary.csv')
    entry = lexicon.loc[lexicon.strongs_no_prefix==entry_id]
    return render(request, 'lexicon/view_entry_alignment.html', {'entry':entry.to_html(index=False) })


def list_entries(request):
    if request.POST:
        #TODO needs form validation
        search = request.POST.get('input')
        if search.startswith('H') or search.startswith('G') or search.startswith('A'):
            results = Source.objects.filter(strongs_no_prefix=search).values('lemma', 'strongs_no_prefix').distinct('strongs_no_prefix').order_by('strongs_no_prefix')
        else:
            results = Source.objects.filter(lemma=search).distinct('lemma').order_by('lemma')
        if results.count() == 0:
            #NOTE actually this is a search engine for alignments
            results = Source.objects.filter(target__target_token__icontains=search).values('strongs_no_prefix', 'lemma', 'strongs_count').annotate(hit_count=Count('strongs_no_prefix')).order_by('-hit_count', '-strongs_count') #.distinct('strongs_no_prefix')
        return render(request, 'lexicon/list_entries.html', {'results': results })
    
    
    sources = Source.objects.all()[:50].values('strongs_no_prefix', 'strongs_count', 'lemma')
    strongs = {itm['strongs_no_prefix']:str(itm['strongs_count']) + 'x ({})'.format(itm['lemma']) for itm in sources if itm['strongs_count']}
    greek = Source.objects.filter(strongs_no_prefix__startswith='G')[:50].values('strongs_no_prefix', 'strongs_count', 'lemma')
    greek = {itm['strongs_no_prefix']:str(itm['strongs_count']) + 'x ({})'.format(itm['lemma']) for itm in greek if itm['strongs_count']}

        
    return render(request, 'lexicon/list_entries.html', {'entries': strongs, 'greek':greek})


def view_verse(request, book, chapter, verse):
    source = Source.objects.filter(book=book, chapter=chapter, verse=verse)
    target = Target.objects.filter(book=book, chapter=chapter, verse=verse)
    notes = Notes.objects.filter(book=book, chapter=chapter, verse=verse)
    #TODO hardcoded
    try:
        book_nr = int(book.split('-')[0])
        if book_nr > 40:
            font = 'gk'
        else:
            font = 'hb'
    except:
        font = '' 

    context = {
        'source':source,
        'target':target,
        'book':book,
        'chapter':chapter,
        'verse':verse,
        'notes':notes,
        'font':font,
        }
    return render(request, 'lexicon/view_verse.html', context)
