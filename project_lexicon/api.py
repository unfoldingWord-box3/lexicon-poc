from rest_framework import views, viewsets
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from serializers import SourceSerializer, SimpleVerseSerializer, TargetSerializer, AlignmentSerializer, WordsSerializer, StrongsM2MSerializer, NotesSerializer, LexiconSerializer, GlossesSerializer
from lexicon.models import Source, Target, Alignment, Words, StrongsM2M, Notes, Lexicon, Glosses


class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('long'):
            return ['$long']
        return super(CustomSearchFilter, self).get_search_fields(view, request)


class GlossesViewSet(viewsets.ModelViewSet):
    queryset = Glosses.objects.all()
    serializer_class = GlossesSerializer
    filter_backends = ( DjangoFilterBackend, CustomSearchFilter)
    filterset_fields = ['strongs', 'lemma']
    search_fields = ['$brief']  # add &long to the get params to search in the 'long' field


class SourceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows verses to be viewed.
    """
    queryset = Source.objects.all() # filter(book='01-GEN', chapter=1, verse=1)
    serializer_class = SourceSerializer
    filterset_fields = ['book', 'chapter', 'verse', 'strongs_no_prefix', 'lemma']
    # search_fields = ['token',]


# class SimpleVerse(viewsets.ModelViewSet):
#     """
#     API endpoint that allows verses to be viewed.
#     """
#     queryset = Source.objects.all() # filter(book='01-GEN', chapter=1, verse=1)
#     serializer_class = SimpleVerseSerializer
#     filterset_fields = ['book', 'chapter', 'verse']
#
#     def list(self, request, *args, **kwargs):
#         qs = self.get_queryset()[:500]
#         text = [itm['token'] for itm in qs.values('token')]
#         return Response({'response': text})

#     def retrieve(self, request, *args, **kwargs):
#         return Response({'response': 'my custom JSON'})


class TargetViewSet(viewsets.ModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer
    filterset_fields = ['book', 'chapter', 'verse']


class AlignmentViewSet(viewsets.ModelViewSet):
    queryset = Alignment.objects.all()
    # export book, chapter, verse, source tokens, target tokens, source->target mapping
    serializer_class = AlignmentSerializer
    filterset_fields = ['alg_has_gap', 'roots']


class WordsViewSet(viewsets.ModelViewSet):
    queryset = Words.objects.all()
    serializer_class = WordsSerializer


class StrongsM2MViewSet(viewsets.ModelViewSet):
    queryset = StrongsM2M.objects.all()
    serializer_class = StrongsM2MSerializer    
    filterset_fields = ['number']


class NotesViewSet(viewsets.ModelViewSet):
    queryset = Notes.objects.all()
    serializer_class = NotesSerializer
    filterset_fields = ['book', 'chapter', 'verse', 'supportreference', 'source__strongs_no_prefix']


class LexiconViewSet(viewsets.ModelViewSet):
    queryset = Lexicon.objects.all()
    serializer_class = LexiconSerializer
    filterset_fields = ['strongs']



# Notes.objects.values('supportreference').annotate(count = Count('supportreference')).order_by('-count')