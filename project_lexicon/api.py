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
    queryset = Source.objects.filter(book='01-GEN', chapter=1, verse=1)
    serializer_class = SourceSerializer

class TargetViewSet(viewsets.ModelViewSet):
    queryset = Target.objects.all()[:50]
    serializer_class = TargetSerializer