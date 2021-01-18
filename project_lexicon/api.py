from rest_framework import views, viewsets

from serializers import SourceSerializer, TargetSerializer, AlignmentSerializer, TwSerializer, StrongsM2MSerializer
from lexicon.models import Source, Target, Alignment, Tw, StrongsM2M

class SourceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows verses to be viewed.
    """
    queryset = Source.objects.all() # filter(book='01-GEN', chapter=1, verse=1)
    serializer_class = SourceSerializer
    filterset_fields = ['book', 'chapter', 'verse']
    # search_fields = ['token',]


class TargetViewSet(viewsets.ModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer
    filterset_fields = ['book', 'chapter', 'verse']


class AlignmentViewSet(viewsets.ModelViewSet):
    queryset = Alignment.objects.all()
    # export book, chapter, verse, source tokens, target tokens, source->target mapping
    serializer_class = AlignmentSerializer


class TwViewSet(viewsets.ModelViewSet):
    queryset = Tw.objects.all()
    # export book, chapter, verse, source tokens, target tokens, source->target mapping
    serializer_class = TwSerializer


class StrongsM2MViewSet(viewsets.ModelViewSet):
    queryset = StrongsM2M.objects.all()
    # export book, chapter, verse, source tokens, target tokens, source->target mapping
    serializer_class = StrongsM2MSerializer    
    filterset_fields = ['number']