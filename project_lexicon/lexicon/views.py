import json
import random
from collections import OrderedDict
from itertools import groupby
import copy
import pandas as pd

from django.shortcuts import render
from django.db.models import Count

from .models import Source, Target, Alignment, StrongsM2M, Notes, Words


# UTILS 

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


def get_concordance_old(alg_ids, idx, alignment_df, model, id_column, token_column, token_prefix_column=None, window=4):
    samples = []
    samples_ids = {}
    sample_highlights = []
    for id in alg_ids:
        selection = alignment_df.loc[alignment_df.alg_id==id, id_column].tolist()
        start = min(selection) - window
        end = max(selection) + window
        samples_ids[idx] = list(range(start,end))
        sample_highlights.extend(selection)
            
        ids = [i for itm in samples_ids.values() for i in itm]
        if token_prefix_column:
            s = model.objects.values(token_column, token_prefix_column, 'id').filter(id__in=ids)
        else:
            s = model.objects.values(token_column, 'id').filter(id__in=ids)
        # print(s)
        s = pd.DataFrame(s)
        if token_prefix_column:
            s[token_column] = s[token_prefix_column] + s[token_column]
        s.loc[s.id.isin(sample_highlights), token_column] = '<span class="hl">'+s[token_column]+'</span>'

        for key,val in samples_ids.items():
            samples.append(''.join(s.loc[s.id.isin(val)][token_column].fillna('').tolist()))

    return samples


def expand_window(li, window=5):
    output = []
    for itm in li:
        for i in range(-window,window+1):
            output.append(itm+i)
    return set(output)


def build_concordance(token_ids, window_tokens, window=5):
    concordance = []  

    for i in range(min(token_ids)-window, max(token_ids)+window+1):
        try:
            token = window_tokens[i]
            if i in token_ids:
                #TODO add prefix
                token = '<span class="hl">' + token + '</span>'
            if token:  # some cases are None
                concordance.append(token)
        except:
            continue
    return concordance


# VIEWS 

def demo_entry(request):
    return render(request, 'lexicon/demo_entry.html')


def list_entries(request):
    sources = Source.objects.all()[:50].values('strongs_no_prefix', 'strongs_count', 'lemma')
    strongs = {itm['strongs_no_prefix']:str(itm['strongs_count']) + 'x ({})'.format(itm['lemma']) for itm in sources if itm['strongs_count']}
    all_numbers = None
    return render(request, 'lexicon/list_entries.html', {'entries': strongs, 'all_numbers':all_numbers})


def alt_view_entry(request, entry_id):
    
    try:
        lemma = Source.objects.filter(strongs_no_prefix=entry_id)[0].lemma
    except:
        lemma = None
    font = get_font(entry_id)

    result = Alignment.objects.filter(source__strongs_no_prefix=entry_id).values('id', 'alg_id', 'source', 'source__token', 'source__morph', 'target', 'target__target_token', 'roots', 'source_blocks', 'target_blocks')
    source_ids = [itm['source'] for itm in result]
    target_ids = [itm['target'] for itm in result]

    source_ids_w_window = expand_window(source_ids)
    source_window_tokens = dict(Source.objects.filter(id__in=source_ids_w_window).values_list('id', 'token'))

    target_ids_w_window = expand_window(target_ids)
    target_window_tokens = dict(Target.objects.filter(id__in=target_ids_w_window).values_list('id', 'target_token'))

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
    table = df.to_html()

    # start splitting out the senses
    COLUMN = 'target_blocks'
    if request.GET.get('roots'):
        COLUMN = 'roots'
    
    # now regroup per sense
    frequencies = df.drop_duplicates('alg_id').groupby(COLUMN).size().sort_values(ascending=False)
    print(frequencies)
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

    return render(request, 'lexicon/view_entry.html', {'table':table,
        'senses':senses,
        'entry':entry_id,
        'lemma': lemma,
        'font': font,})


def view_entry(request, entry_id):
    aligs = Alignment.objects.filter(source__strongs_no_prefix=entry_id).values()
    try:
        lemma = Source.objects.filter(strongs_no_prefix=entry_id)[0].lemma
    except:
        lemma = None
    font = get_font(entry_id)

    COLUMN = 'target_blocks'
    if request.GET.get('roots'):
        COLUMN = 'roots'
    
    alignments = pd.DataFrame(aligs)
    frequencies = alignments.drop_duplicates('alg_id').groupby(COLUMN).size().sort_values(ascending=False)
    
    # senses_text = alignments.groupby('roots').size().sort_values(ascending=False).index.tolist()
    senses_text = alignments.groupby(COLUMN).size().sort_values(ascending=False).index.tolist()

    senses = []
    for idx,freq in enumerate(frequencies.items(), start=1):
        # order, color, icon, frequency, 5 samples      
        sense, frequency = freq[0].strip(), freq[1]

        alg = alignments.loc[alignments[COLUMN]==freq[0]]
        # print(alg)
        alg_ids = alg.alg_id.unique().tolist()
        # print(alg_ids)
        if len(alg_ids) > 5:
            alg_ids = random.sample(alg_ids, k=5)

        target_samples = get_concordance_old(alg_ids, idx, alignments, Target, 'target_id', 'target_token', 'target_token_prefix', window=8)
        source_samples = get_concordance_old(alg_ids, idx, alignments, Source, 'source_id', 'token')

        senses.append({'freq':frequency,
                       'sense':sense,
                       'color':COLOR_SCALE[idx],
                       'order':idx,
                       'icon':ICON_SCALE[idx],
                       'target_samples':target_samples,
                       'source_samples':source_samples,
        })
    
    tw_related_items = StrongsM2M.objects.filter(number=entry_id).values_list('related_number')
    strongs = Source.objects.filter(strongs_no_prefix__in=tw_related_items).values_list('strongs_no_prefix', 'lemma').distinct()
    tw_related_items = dict(strongs)
    
    target_blocks = frequencies.index.tolist()
    # print(target_blocks)
    # .values('lemma', 'strongs')
    if COLUMN == 'roots':
        sense_related_items = Alignment.objects.filter(roots__in=target_blocks).select_related('source').distinct()
        sense_related_items = None
    else:
        # sense_related_items = Alignment.objects.filter(target_blocks__in=target_blocks).select_related('source').distinct()
        sense_related_items = None
    sense_dict = {}
    # for itm in sense_related_items:
    #     sense_dict[itm.source.strongs_no_prefix] = itm.source.lemma

    return render(request, 'lexicon/view_entry.html', 
        {'entry':entry_id,
         'lemma': lemma,
         'font': font,
         'senses_text': senses_text,
         'senses': senses,
         'tw_related_items': tw_related_items,
         'sense_related_items': sense_dict,
          })


def list_entries_df(request):
    lexicon = pd.read_csv('../data/csv/dictionary.csv')
    # all_numbers = json.dumps({nr:nr for nr in lexicon.strongs.unique().tolist()})
    all_numbers = json.dumps(lexicon.strongs_no_prefix.unique().tolist())
    strongs = lexicon.strongs_no_prefix.value_counts().sort_index().sample(50)
    return render(request, 'lexicon/list_entries.html', {'entries': strongs, 'all_numbers':all_numbers})


def view_entry_df(request, entry_id):
    lexicon = pd.read_csv('../data/csv/dictionary.csv')
    ALIGNMENT = pd.read_csv('../data/csv/alignment.csv')
    entry = lexicon.loc[lexicon.strongs_no_prefix==entry_id]
    lemma = entry.loc[:,'lemma'].iloc[0]
    font = get_font(entry_id)

    senses_text = entry.groupby('roots').size().sort_values(ascending=False).index.tolist()
    
    senses = []
    frequencies = entry.groupby('target_blocks').size().sort_values(ascending=False)

    for idx,freq in enumerate(frequencies.items(), start=1):
        # order, color, icon, frequency, 5 samples      
        sense, frequency = freq[0].strip(), freq[1]
        examples_idx = ALIGNMENT.loc[(ALIGNMENT.strongsNoPrefix==entry_id) & (ALIGNMENT.target_token.str.strip()==sense)].index.tolist()
        samples = []
        for example in examples_idx[:5]:
            case = ALIGNMENT.loc[example-7:example+7]
            case.loc[example, 'target_token'] = '<span class="hl">' + case.loc[example, 'target_token'] + '</span>'
            samples.append(''.join(case.target_token.fillna('').tolist()))

        senses.append({'freq':frequency,
                       'sense':sense,
                       'color':COLOR_SCALE[idx],
                       'order':idx,
                       'icon':ICON_SCALE[idx],
                       'samples':samples,
        })

    return render(request, 'lexicon/view_entry.html', 
        {'entry':entry_id,
         'lemma': lemma,
         'font': font,
         'senses_text': senses_text,
         'senses': senses,
          })


def view_entry_alignment(request, entry_id):
    lexicon = pd.read_csv('../data/csv/dictionary.csv')
    entry = lexicon.loc[lexicon.strongs_no_prefix==entry_id]
    return render(request, 'lexicon/view_entry_alignment.html', {'entry':entry.to_html(index=False) })


def view_verse(request, book, chapter, verse):
    source = Source.objects.filter(book=book, chapter=chapter, verse=verse)
    target = Target.objects.filter(book=book, chapter=chapter, verse=verse)
    notes = Notes.objects.filter(book=book, chapter=chapter, verse=verse)

    context = {
        'source':source,
        'target':target,
        'book':book,
        'chapter':chapter,
        'verse':verse,
        'notes':notes,
        }
    return render(request, 'lexicon/view_verse.html', context)
