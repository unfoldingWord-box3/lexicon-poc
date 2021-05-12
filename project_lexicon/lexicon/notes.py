import re

from django.db.models import query
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView
from django.urls import reverse
from django.http import QueryDict

from .views import get_font 
from .models import Notes, Source, Target
from .filters import NotesFilter


class NotesListView(ListView):
    model = Notes
    context_object_name = 'notes'
    template_name = 'lexicon/list_notes.html'

    def get_queryset(self):
        qs = super().get_queryset()
        filtered = NotesFilter(self.request.GET, queryset=qs)
        return filtered.qs.distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['filter'] = NotesFilter(self.request.GET)
        
        query_dict = QueryDict(mutable=True)
        for key,val in self.request.GET.items():
            # removing page here, might have to add pagination to this view in its own right
            if val and key != 'page':
                query_dict[key] = val
        
        context['base_page'] = reverse('navigate_notes') + '?' + query_dict.urlencode()

        return context


class NotesDetailViewPerSearch(NotesListView):
    paginate_by = 1
    template_name = 'lexicon/notes_detail_per_search.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        '''
        Here's the magic:

        Although this is a LIST View it really is used to only display a SINGLE object
        because it is paginated by 1.
        
        This is done so the entire queryset can be filtered by the user and the user can then
        go through each item in said queryset. 

        This means that we need to add the actual information based on the paginated queryset here
        and not just the basic queryset. 
        '''
        qs = self.get_queryset()
        # (<django.core.paginator.Paginator object at 0x7f1a605f99a0>, <Page 2 of 4>, <QuerySet [ix79: figs-euphemism]>, True)
        paginator = self.paginate_queryset(qs, self.get_paginate_by(qs))
        
        try:
            # gets the first element of the queryset of the selected page
            note = paginator[2].first()
        except: 
            # a fallback to show something, it will display the wrong text though (but the right note)
            note = self.get_queryset().first()

        context['source'] = Source.objects.filter(book=note.book, chapter=note.chapter, verse=note.verse)
        book_nr = int(note.book.split('-')[0])
        if book_nr > 40:
            font = 'gk'
        else:
            font = 'hb'
        context['font'] = font
        context['source'].first().strongs_no_prefix
        context['target'] = Target.objects.filter(book=note.book, chapter=note.chapter, verse=note.verse)

        # make sure you pass the GET parameters along
        query_dict = QueryDict(mutable=True)
        for key,val in self.request.GET.items():
            if val and key != 'page':
                query_dict[key] = val

        context['url'] = reverse('navigate_notes') + '?' + query_dict.urlencode()
        context['base_page'] = reverse('list_notes') + '?' + query_dict.urlencode()

        # prepare some nagivation
        page = paginator[1]
        if page.has_previous(): 
            context['previous_page'] = page.previous_page_number()
        if page.has_next():
            context['next_page'] = page.next_page_number()

        return context


class NotesDetailView(DetailView):
    model = Notes
    pk_url_kwarg = 'index'
    context_object_name = 'note'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        note = self.object
        context['source'] = Source.objects.filter(book=note.book, chapter=note.chapter, verse=note.verse)
        book_nr = int(note.book.split('-')[0])
        if book_nr > 40:
            font = 'gk'
        else:
            font = 'hb'
        context['font'] = font
        context['source'].first().strongs_no_prefix
        context['target'] = Target.objects.filter(book=note.book, chapter=note.chapter, verse=note.verse)
        context['previous_note'] = Notes.objects.filter(index__lt=note.index).order_by('-index').first()
        context['next_note'] = Notes.objects.filter(index__gt=note.index).order_by('index').first()

        return context


class NotesUpdateView(UpdateView):
    model = Notes
    pk_url_kwarg = 'index'
    context_object_name = 'note'
    fields = 'supportreference annotation sourceword'.split()

