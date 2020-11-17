# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Alignment(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    id = models.BigIntegerField(blank=True, null=True)
    target_id = models.BigIntegerField(blank=True, null=True)
    source_id = models.BigIntegerField(blank=True, null=True)
    alg_id = models.TextField(blank=True, null=True)
    alg = models.TextField(blank=True, null=True)
    alg_has_gap = models.BooleanField(blank=True, null=True)
    source_blocks = models.TextField(blank=True, null=True)
    target_blocks = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alignment'


class Source(models.Model):
    level_0 = models.BigIntegerField(blank=True, null=True)
    id = models.BigIntegerField(blank=True, null=True)
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
    tw_id = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'source'


class StrongsM2M(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    number = models.TextField(blank=True, null=True)
    related_number = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'strongs_m2m'


class Target(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    id = models.BigIntegerField(blank=True, null=True)
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

    class Meta:
        managed = False
        db_table = 'target'


class Tw(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    header = models.TextField(blank=True, null=True)
    definition = models.TextField(blank=True, null=True)
    suggestions = models.TextField(blank=True, null=True)
    refs = models.TextField(blank=True, null=True)
    strongs = models.TextField(blank=True, null=True)
    id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tw'
