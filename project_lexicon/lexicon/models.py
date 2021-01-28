from django.db import models

#TODO update the nameing scheme: singular, abstract


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

    class Meta:
        managed = False
        db_table = 'source'
        verbose_name_plural = 'Source'
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