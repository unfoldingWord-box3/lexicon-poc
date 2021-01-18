from rest_framework import serializers, views, viewsets

from lexicon.models import Source, Target


class SourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Source
        fields = ['token', 'book', 'chapter', 'verse']


class TargetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Target
        fields = ['token', 'book', 'chapter', 'verse']


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
