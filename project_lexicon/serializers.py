from rest_framework import serializers

from lexicon.models import Source, Target, Alignment, Tw, StrongsM2M, Notes


class SourceSerializer(serializers.HyperlinkedModelSerializer):
    tw = serializers.HyperlinkedRelatedField(source='tw.id', read_only=True, view_name="tw-detail")
    notes = serializers.HyperlinkedRelatedField(source='notes_set', read_only=True, view_name="notes-detail", many=True)

    class Meta:
        model = Source
        # fields = ['token', 'book', 'chapter', 'verse']
        fields = '__all__'
        # exclude = ['tw',]


class TargetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Target
        # fields = ['token', 'target_token', 'book', 'chapter', 'verse']
        fields = '__all__'


class AlignmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Alignment
        fields = '__all__'
        # fields = ['id', ]


class TwSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tw
        fields = '__all__'
        # fields = ['id', ]


class StrongsM2MSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StrongsM2M
        fields = '__all__'
        # fields = ['id', ]

class NotesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notes
        fields = '__all__'
        # fields = ['id', ]