from rest_framework import serializers

from lexicon.models import Source, Target, Alignment, Words, StrongsM2M, Notes, Lexicon


class SourceSerializer(serializers.HyperlinkedModelSerializer):
    words = serializers.HyperlinkedRelatedField(source='words.id', read_only=True, view_name="words-detail")
    notes = serializers.HyperlinkedRelatedField(source='notes_set', read_only=True, view_name="notes-detail", many=True)
    #TODO replace this by an actual ForeignKey in the models field
    lexicon = serializers.HyperlinkedRelatedField(source='strongs_no_prefix', read_only=True, view_name="lexicon-detail")

    class Meta:
        model = Source
        fields = '__all__'


class SimpleVerseSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Source
        fields = ['token', 'book', 'chapter', 'verse']


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


class WordsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Words
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


class LexiconSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lexicon
        fields = '__all__'