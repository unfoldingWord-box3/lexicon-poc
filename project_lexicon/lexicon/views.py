import pandas as pd

from django.shortcuts import render


def demo_entry(request):
    return render(request, 'lexicon/demo_entry.html')


def list_entries(request):
    lexicon = pd.read_csv('../data/alignment/dictionary.csv')
    strongs = lexicon.strongs.value_counts().sort_index()
    # strongs = sorted(strongs)
    return render(request, 'lexicon/list_entries.html', {'entries': strongs})


def view_entry(request, entry_id):
    lexicon = pd.read_csv('../data/alignment/dictionary.csv')
    entry = lexicon.loc[lexicon.strongs==entry_id]
    lemma = entry.loc[:,'lemma'].iloc[0]
    font = entry_id[0]
    if font=='A': font='H'
    return render(request, 'lexicon/view_entry.html', 
        {'entry':entry_id,
         'lemma': lemma,
         'font': font
          })


def view_entry_alignment(request, entry_id):
    lexicon = pd.read_csv('../data/alignment/dictionary.csv')
    entry = lexicon.loc[lexicon.strongs==entry_id]
    return render(request, 'lexicon/view_entry_alignment.html', {'entry':entry.to_html(index=False) })