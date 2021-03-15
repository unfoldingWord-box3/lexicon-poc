from rest_framework import serializers
from django_restql.mixins import DynamicFieldsMixin

from lexicon.models import (Source, 
    Target, Alignment, Words, 
    StrongsM2M, Notes, Lexicon, 
    Glosses, Question, BDB, 
    BDB_senses, BDB_strongs,
)


'''
The DynamicFieldsMixin makes GraphQL queries possible. 

/api/source/?book=06-JOS&chapter=&verse=&strongs_no_prefix=&query={book,chapter,verse,token,alignments{target{target_token,index}},words{category}}
'''


class BDBSerializer(DynamicFieldsMixin, serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = BDB
        fields = '__all__'


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = Question
        fields = '__all__'


class GlossesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Glosses
        fields = '__all__'


class WordsSerializer(DynamicFieldsMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Words
        fields = '__all__'
        # fields = ['id', ]


class TargetSerializer(DynamicFieldsMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Target
        # fields = ['token', 'target_token', 'book', 'chapter', 'verse']
        fields = '__all__'


class AlignmentSerializer(DynamicFieldsMixin, serializers.HyperlinkedModelSerializer):
    target = TargetSerializer(many=False)

    class Meta:
        model = Alignment
        fields = '__all__'
        # fields = ['id', ]


class SimpleSourceSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Source
        fields = "book chapter verse token id url morph lemma strongs".split()



class SourceSerializer(DynamicFieldsMixin, serializers.HyperlinkedModelSerializer):
    words_url = serializers.HyperlinkedRelatedField(source='words.id', read_only=True, view_name="words-detail")
    words = WordsSerializer(many=False, read_only=True) 
    notes = serializers.HyperlinkedRelatedField(source='notes_set', read_only=True, view_name="notes-detail", many=True)
    #TODO replace this by an actual ForeignKey in the models field
    lexicon = serializers.HyperlinkedRelatedField(source='strongs_no_prefix', read_only=True, view_name="lexicon-detail")
    alignments = AlignmentSerializer(many=True, source='alignment_set')

    class Meta:
        model = Source
        fields = '__all__'


class SimpleVerseSerializer(DynamicFieldsMixin, serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Source
        fields = ['token', 'book', 'chapter', 'verse']


class StrongsM2MSerializer(DynamicFieldsMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StrongsM2M
        fields = '__all__'
        # fields = ['id', ]


class NotesSerializer(DynamicFieldsMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notes
        fields = '__all__'
        # fields = ['id', ]


class LexiconSerializer(DynamicFieldsMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lexicon
        fields = '__all__'