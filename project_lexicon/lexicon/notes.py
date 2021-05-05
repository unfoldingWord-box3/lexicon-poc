from django.views.generic import DetailView

from .views import get_font 
from .models import Notes, Source, Target


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
        return context
