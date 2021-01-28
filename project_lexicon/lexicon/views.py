import json
import random
from collections import OrderedDict

import pandas as pd

from django.shortcuts import render
from django.db.models import Count

from .models import Source, Target, Alignment, StrongsM2M, Notes


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


def demo_entry(request):
    return render(request, 'lexicon/demo_entry.html')


def list_entries(request):
    sources = Source.objects.all()[:50].values('strongs_no_prefix', 'lemma').annotate(count=Count('strongs_no_prefix'))
    strongs = {itm['strongs_no_prefix']:str(itm['count']) + 'x ({})'.format(itm['lemma']) for itm in sources if itm['count']}
    all_numbers = None
    return render(request, 'lexicon/list_entries.html', {'entries': strongs, 'all_numbers':all_numbers})


def get_concordance(alg_ids, idx, alignment_df, model, id_column, token_column, token_prefix_column=None, window=4):
    samples = []
    samples_ids = {}
    sample_highlights = []
    for id in alg_ids:
        selection = alignment_df.loc[alignment_df.id==id, id_column].tolist()
        start = min(selection) - window
        end = max(selection) + window
        samples_ids[idx] = list(range(start,end))
        sample_highlights.extend(selection)
            
        ids = [i for itm in samples_ids.values() for i in itm]
        if token_prefix_column:
            s = model.objects.values(token_column, token_prefix_column, 'id').filter(id__in=ids)
        else:
            s = model.objects.values(token_column, 'id').filter(id__in=ids)
        s = pd.DataFrame(s)
        if token_prefix_column:
            s[token_column] = s[token_prefix_column] + s[token_column]
        s.loc[s.id.isin(sample_highlights), token_column] = '<span class="hl">'+s[token_column]+'</span>'
        
        for key,val in samples_ids.items():
            samples.append(''.join(s.loc[s.id.isin(val)][token_column].fillna('').tolist()))
    return samples
                

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


def view_entry(request, entry_id):
    aligs = Alignment.objects.filter(source__strongs_no_prefix=entry_id)
    try:
        lemma = Source.objects.filter(strongs_no_prefix=entry_id).first().lemma
    except:
        lemma = None
    font = get_font(entry_id)

    COLUMN = 'target_blocks'
    if request.GET.get('roots'):
        COLUMN = 'roots'
    
    alignments = pd.DataFrame(aligs.values())
    frequencies = alignments.drop_duplicates('alg_id').groupby(COLUMN).size().sort_values(ascending=False)
    
    # senses_text = alignments.groupby('roots').size().sort_values(ascending=False).index.tolist()
    senses_text = alignments.groupby(COLUMN).size().sort_values(ascending=False).index.tolist()

    senses = []
    for idx,freq in enumerate(frequencies.items(), start=1):
        # order, color, icon, frequency, 5 samples      
        sense, frequency = freq[0].strip(), freq[1]

        alg = alignments.loc[alignments[COLUMN]==freq[0]]
        alg_ids = alg.id.unique().tolist()
        if len(alg_ids) > 5:
            alg_ids = random.sample(alg_ids, k=5)

        target_samples = get_concordance(alg_ids, idx, alignments, Target, 'target_id', 'target_token', 'target_token_prefix', window=8)
        source_samples = get_concordance(alg_ids, idx, alignments, Source, 'source_id', 'token')

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
    else:
        sense_related_items = Alignment.objects.filter(target_blocks__in=target_blocks).select_related('source').distinct()
    sense_dict = {}
    for itm in sense_related_items:
        sense_dict[itm.source.strongs_no_prefix] = itm.source.lemma

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
    lexicon = pd.read_csv('../data/alignment/dictionary.csv')
    # all_numbers = json.dumps({nr:nr for nr in lexicon.strongs.unique().tolist()})
    all_numbers = json.dumps(lexicon.strongs.unique().tolist())
    strongs = lexicon.strongs.value_counts().sort_index().sample(50)
    return render(request, 'lexicon/list_entries.html', {'entries': strongs, 'all_numbers':all_numbers})


def view_entry_df(request, entry_id):
    lexicon = pd.read_csv('../data/alignment/dictionary.csv')
    ALIGNMENT = pd.read_csv('../data/alignment/alignment.csv')
    entry = lexicon.loc[lexicon.strongs==entry_id]
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
    lexicon = pd.read_csv('../data/alignment/dictionary.csv')
    entry = lexicon.loc[lexicon.strongs==entry_id]
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
