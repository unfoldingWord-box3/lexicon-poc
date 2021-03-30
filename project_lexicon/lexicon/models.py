import json
from django.db import models

#TODO update the nameing scheme: singular, abstract, identical
#TODO create a real link between source words and the lexicon, and not just via the API


class BDB(models.Model):
    index = models.BigIntegerField(blank=True)
    bdb = models.TextField(blank=True, primary_key=True)
    pos = models.TextField(blank=True, null=True)
    main_gloss = models.TextField(blank=True, null=True)
    refs = models.TextField(blank=True, null=True)
    full = models.TextField(blank=True, null=True)
    text_only = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.bdb

    class Meta:
        managed = False
        db_table = 'bdb'
        verbose_name = 'BDB'
        verbose_name_plural = 'BDB'


class BDB_senses(models.Model):
    index = models.BigIntegerField(blank=True, primary_key=True)
    bdb = models.ForeignKey(BDB, null=True, on_delete=models.SET_NULL, db_column='bdb')
    idx = models.BigIntegerField(blank=True, null=True)
    bold = models.TextField(blank=True, null=True)
    gloss = models.TextField(blank=True, null=True)
    refs = models.TextField(blank=True, null=True)
    nr_of_refs = models.BigIntegerField(blank=True, null=True)

    @property
    def parsed_refs(self):
        if not self.refs:
            return None
        refs = json.loads(json.loads(self.refs))

        # source = Source.objects.filter(strongs_no_prefix__isin=)

        output = []
        for ref in refs:
            number,text = ref
            output.append(number)
        return output

    def __str__(self) -> str:
        return '{}: {}'.format(self.bdb, self.bold)


    class Meta:
        managed = False
        db_table = 'bdb_senses'
        ordering = ['idx']
        verbose_name = 'BDB senses'
        verbose_name_plural = 'BDB senses'


class BdbSenseToSource(models.Model):
    index = models.BigIntegerField(blank=True, primary_key=True)
    sense = models.ForeignKey(BDB_senses, blank=True, null=True, on_delete=models.SET_NULL, db_column='sense')
    bdb = models.ForeignKey(BDB, blank=True, null=True, on_delete=models.SET_NULL, db_column='bdb')
    source = models.ForeignKey('Source', blank=True, null=True, on_delete=models.SET_NULL, db_column='source')
    simple_refs = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return 'BDB {} sense {} link: {}'.format(self.bdb, self.sense, self.index)

    class Meta:
        managed = False
        db_table = 'bdb_sense_to_source'
        verbose_name = 'BDB links with source'
        verbose_name_plural = 'BDB links with source'


class BDB_strongs(models.Model):
    index = models.BigIntegerField(blank=True, primary_key=True)
    bdb = models.ForeignKey(BDB, db_column='bdb', on_delete=models.SET_NULL, null=True)
    strongs = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bdb_strongs'
        verbose_name = 'BDB to strongs'
        verbose_name_plural = 'BDB to strongs'


class Collocations(models.Model):
    node = models.CharField(max_length=250, primary_key=True)
    context = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'collocations'
        verbose_name = 'Collocation'
        verbose_name_plural = 'Collocations'


class Dodson(models.Model):
    index = models.BigIntegerField(blank=True, primary_key=True)
    strongs = models.TextField(blank=True, null=True)
    goodrick_kohlenberger = models.TextField(db_column='Goodrick-Kohlenberger', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    lemma = models.TextField(blank=True, null=True)
    brief = models.TextField(blank=True, null=True)
    long = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dodson'
        verbose_name = 'Dodson'
        verbose_name_plural = 'Dodson'        


class Glosses(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    strongs = models.TextField(blank=True, primary_key=True)
    brief = models.TextField(blank=True, null=True)
    long = models.TextField(blank=True, null=True)
    lemma = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'glosses'
        verbose_name = 'Gloss'
        verbose_name_plural = 'Glosses'        


class Source(models.Model):
    id = models.BigIntegerField(blank=True, primary_key=True)
    level_0 = models.BigIntegerField(blank=True, null=True)
    index = models.BigIntegerField(blank=True, null=True)
    source_token = models.TextField(blank=True, null=True)
    book = models.TextField(blank=True, null=True)
    chapter = models.BigIntegerField(blank=True, null=True)
    verse = models.BigIntegerField(blank=True, null=True)
    token = models.TextField(blank=True, null=True)
    token_prefix = models.TextField(blank=True, null=True)
    morph = models.TextField(blank=True, null=True)
    lemma = models.TextField(blank=True, null=True)
    strongs = models.TextField(blank=True, null=True)
    strongs_no_prefix = models.TextField(blank=True, null=True)
    has_prefix = models.BooleanField(blank=True, null=True)
    translation_word = models.TextField(blank=True, null=True)
    orig_id = models.BigIntegerField(blank=True, null=True)
    occs = models.BigIntegerField(blank=True, null=True)
    occ = models.BigIntegerField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    # tw_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    words = models.ForeignKey('Words', blank=True, null=True, on_delete=models.SET_NULL, db_column='tw_id')  #FIXME in data creation script
    strongs_count = models.BigIntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return '{}'.format(self.id)


    class Meta:
        managed = False
        db_table = 'source'
        verbose_name_plural = 'Source'
        ordering = ['id']
        # indexes = [
        #     models.Index(fields=['id',]),
        #     models.Index(fields=['strongs',]),
        #     models.Index(fields=['strongs_no_prefix',]),
        #     models.Index(fields=['token',]),
        #     models.Index(fields=['book','chapter','verse']),
        # ]

    def __repr__(self):
        return f'{self.id}: {self.token}'


class Target(models.Model):
    id = models.BigIntegerField(blank=True, primary_key=True)
    index = models.BigIntegerField(blank=True, null=True)
    orig_id = models.BigIntegerField(blank=True, null=True)
    token = models.TextField(blank=True, null=True)
    chapter = models.BigIntegerField(blank=True, null=True)
    verse = models.BigIntegerField(blank=True, null=True)
    book = models.TextField(blank=True, null=True)
    alg_id = models.TextField(blank=True, null=True)
    target_token = models.TextField(blank=True, null=True)
    target_token_prefix = models.TextField(blank=True, null=True)
    target_blocks = models.TextField(blank=True, null=True)
    target_occ = models.TextField(blank=True, null=True)
    target_occs = models.TextField(blank=True, null=True)

    source = models.ManyToManyField(Source, through='Alignment')

    class Meta:
        managed = False
        db_table = 'target'
        verbose_name_plural = 'Target'
        ordering = ['id']


    def __str__(self) -> str:
        return '{}'.format(self.id)

    def __repr__(self):
        return f'{self.id}: {self.target_token}'


class Alignment(models.Model):
    #TODO convert this into a through model
    id = models.BigIntegerField(blank=True, primary_key=True)
    index = models.BigIntegerField(blank=True, null=True)
    target = models.ForeignKey(Target, blank=True, null=True, on_delete=models.SET_NULL)
    source = models.ForeignKey(Source, blank=True, null=True, on_delete=models.SET_NULL)
    alg_id = models.TextField(blank=True, null=True)
    alg = models.TextField(blank=True, null=True)
    alg_has_gap = models.BooleanField(blank=True, null=True)
    source_blocks = models.TextField(blank=True, null=True)
    target_blocks = models.TextField(blank=True, null=True)
    # to add a column: ALTER TABLE alignment ADD "roots" TEXT;
    roots = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alignment'
        ordering = ['id']

    def __repr__(self):
        return f'{self.id}: {self.source} -> {self.target}'


class Words(models.Model):
    id = models.BigIntegerField(blank=True, primary_key=True)
    index = models.BigIntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    header = models.TextField(blank=True, null=True)
    definition = models.TextField(blank=True, null=True)
    suggestions = models.TextField(blank=True, null=True)
    refs = models.TextField(blank=True, null=True)
    strongs = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tw'
        verbose_name_plural = 'Words'


    def __repr__(self) -> str:
        return f'{self.name} ({self.category})'


class StrongsM2M(models.Model):
    index = models.BigIntegerField(blank=True, primary_key=True)
    number = models.TextField(blank=True, null=True)
    related_number = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'strongs_m2m'
        verbose_name = 'Strongs internal links'
        verbose_name_plural = 'Strongs internal links'


class Notes(models.Model):  #TODO rename to singular
    index = models.BigIntegerField(blank=True, null=True)
    noteid = models.TextField(db_column='noteID', blank=True, primary_key=True)  # Field name made lowercase.
    book = models.TextField(blank=True, null=True)
    chapter = models.BigIntegerField(blank=True, null=True)
    verse = models.BigIntegerField(blank=True, null=True)
    supportreference = models.TextField(db_column='supportReference', blank=True, null=True)  # Field name made lowercase.
    quote = models.TextField(blank=True, null=True)
    annotation = models.TextField(blank=True, null=True)
    sourceword = models.TextField(db_column='sourceWord', blank=True, null=True)  # Field name made lowercase.
    sourcewordoccurrence = models.BigIntegerField(db_column='sourceWordOccurrence', blank=True, null=True)  # Field name made lowercase.
    source = models.ManyToManyField(Source, through='NotesM2M')

    class Meta:
        managed = False
        db_table = 'notes'
        verbose_name_plural = 'Notes'

    def __repr__(self) -> str:
        return f'{self.noteid}: {self.supportreference}'


class NotesM2M(models.Model):
    index = models.BigIntegerField(blank=True, primary_key=True)
    notes = models.ForeignKey(Notes, blank=True, null=True, on_delete=models.SET_NULL)
    source_word = models.TextField(blank=True, null=True)
    book = models.TextField(blank=True, null=True)
    chapter = models.BigIntegerField(blank=True, null=True)
    verse = models.BigIntegerField(blank=True, null=True)
    occ = models.BigIntegerField(blank=True, null=True)
    source = models.ForeignKey(Source, blank=True, null=True, on_delete=models.SET_NULL)
    token = models.TextField(blank=True, null=True)
    occ_bis = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notesM2M'
        verbose_name = 'Notes link with source'
        verbose_name_plural = 'Notes link with source'


class Lexicon(models.Model):
    index = models.TextField(blank=True, null=True)
    lemma = models.TextField(blank=True, null=True)
    meta = models.TextField(blank=True, null=True)
    word_data = models.TextField(blank=True, null=True)
    etymology = models.TextField(blank=True, null=True)
    senses = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    lexica_used = models.TextField(blank=True, null=True)
    parsed_strongs = models.TextField(blank=True, null=True)
    twot = models.TextField(db_column='TWOT', blank=True, null=True)  # Field name made lowercase.
    bdb = models.TextField(db_column='BDB', blank=True, null=True)  # Field name made lowercase.
    lxx = models.TextField(db_column='LXX', blank=True, null=True)  # Field name made lowercase.
    nr_of_senses = models.BigIntegerField(blank=True, null=True)
    strongs = models.TextField(blank=True, primary_key=True)

    class Meta:
        managed = False
        db_table = 'lexicon'
        verbose_name_plural = 'Lexicon'


class Question(models.Model):
    index = models.BigIntegerField(blank=True, primary_key=True)
    reference = models.TextField(db_column='Reference', blank=True, null=True)  # Field name made lowercase.
    id = models.TextField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    tags = models.TextField(db_column='Tags', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    supportreference = models.TextField(db_column='SupportReference', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    quote = models.TextField(db_column='Quote', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    occurrence = models.TextField(db_column='Occurrence', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    annotation = models.TextField(db_column='Annotation', blank=True, null=True)  # Field name made lowercase.
    book = models.TextField(blank=True, null=True)
    chapter = models.TextField(blank=True, null=True)
    verse = models.TextField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'question'