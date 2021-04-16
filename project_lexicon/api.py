import json
from django.http import JsonResponse

from rest_framework import views, viewsets
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


from serializers import ( SourceSerializer, 
    SimpleVerseSerializer, TargetSerializer, AlignmentSerializer, 
    WordsSerializer, StrongsM2MSerializer, NotesSerializer, 
    LexiconSerializer, GlossesSerializer, QuestionSerializer,
    BDBSerializer, SimpleSourceSerializer
)
from lexicon.models import ( Source, 
    Target, Alignment, Words, 
    StrongsM2M, Notes, Lexicon, 
    Glosses, Question, BDB
)

def source_to_verse(request):
    '''
    This is a hack.

    Takes an id of a source word,
    for instance 321, then searches for that source word,
    gets it book, chapter, and verse,
    to then return either in source or target the entire verse
    '''
    if request.method == 'GET':
        pks = request.GET.getlist('pk')
        pks = [int(pk) for pk in pks]
        source = Source.objects.get(pk=pks[0])
        target = request.GET.get('target', None)
        if target:
            qs = Target.objects.filter(book=source.book, chapter=source.chapter, verse=source.verse)
            output = qs.values_list('target_token')
            # there are not target tokens (only normal tokens)
            if {(None,)} == set(output):
                output = Target.objects.filter(book=source.book, chapter=source.chapter, verse=source.verse).values_list('token')
                output = ' '.join([itm[0] for itm in output if itm[0]])
            else:
                aligned = qs.filter(source__in=pks).values_list('id')
                if aligned: 
                    aligned = [itm[0] for itm in aligned]
                output = []
                for itm in qs.values('target_token', 'id'):
                    if itm['id'] in aligned:
                        output.append('<span class="hl">' + itm['target_token'] + '</span>')
                    else:
                        output.append(itm['target_token'])              
                output = ''.join([itm for itm in output if itm])
        else:
            output = Source.objects.filter(book=source.book, chapter=source.chapter, verse=source.verse).values_list('token')
            output = ''.join([itm[0] for itm in output if itm[0]])
       
        return JsonResponse(json.dumps(output, ensure_ascii=False), safe=False)


class BDBViewSet(viewsets.ModelViewSet):
    queryset = BDB.objects.all()
    serializer_class = BDBSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['$main_gloss']    


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filterset_fields = ['book', 'chapter', 'verse']


class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('long'):
            return ['$long']
        return super(CustomSearchFilter, self).get_search_fields(view, request)


class GlossesViewSet(viewsets.ModelViewSet):
    queryset = Glosses.objects.all()
    serializer_class = GlossesSerializer
    filter_backends = (DjangoFilterBackend, CustomSearchFilter)
    filterset_fields = ['strongs', 'lemma']
    search_fields = ['$brief']  # add &long to the get params to search in the 'long' field


class SimpleSourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SimpleSourceSerializer
    filterset_fields = ['book', 'chapter', 'verse', 'strongs_no_prefix', 'lemma']


class SourceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows verses to be viewed.
    """
    queryset = Source.objects.all() # filter(book='01-GEN', chapter=1, verse=1)
    serializer_class = SourceSerializer
    filterset_fields = ['book', 'chapter', 'verse', 'strongs_no_prefix', 'lemma', 'token', 'morph']
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
    filterset_fields = ['book', 'chapter', 'verse', 'token']
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ['$token']


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