from django.shortcuts import render


def demo_entry(request):
    return render(request, 'lexicon/demo_entry.html')


def view_entry(request):
    return render(request, 'lexicon/view_entry.html')
