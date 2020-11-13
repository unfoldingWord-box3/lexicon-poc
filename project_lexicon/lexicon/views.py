import json
import pandas as pd
from collections import OrderedDict

from django.shortcuts import render


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
    lexicon = pd.read_csv('../data/alignment/dictionary.csv')
    # all_numbers = json.dumps({nr:nr for nr in lexicon.strongs.unique().tolist()})
    all_numbers = json.dumps(lexicon.strongs.unique().tolist())
    strongs = lexicon.strongs.value_counts().sort_index().sample(50)
    return render(request, 'lexicon/list_entries.html', {'entries': strongs, 'all_numbers':all_numbers})


def view_entry(request, entry_id):
    lexicon = pd.read_csv('../data/alignment/dictionary.csv')
    ALIGNMENT = pd.read_csv('../data/alignment/alignment.csv')
    entry = lexicon.loc[lexicon.strongs==entry_id]
    lemma = entry.loc[:,'lemma'].iloc[0]
    font = entry_id[0]
    if font=='A': font='H'

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