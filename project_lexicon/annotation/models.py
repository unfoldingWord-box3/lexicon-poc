from django.conf import settings
from django.db import models

from lexicon.models import Source


class AnnotationLabel(models.Model):
    name = models.CharField(max_length=50) 
    definition = models.TextField(null=True, blank=True)
    examples = models.TextField(null=True, blank=True)
    extra_rules = models.TextField(null=True, blank=True)
    scheme = models.ForeignKey(
        'AnnotationScheme',
        on_delete=models.CASCADE,
        related_name='labels',
        )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('pk',)


class AnnotationScheme(models.Model):
    name = models.CharField(max_length=200)
    aim = models.TextField()
    annotators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='annotators',
    ) 
    editor_in_chief = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='editors',
        null=True,
        on_delete=models.SET_NULL,
    ) 

    def __str__(self):
        return self.name
    
class Annotation(models.Model):
    source_tokens = models.ManyToManyField(Source)
    label = models.ForeignKey(AnnotationLabel, on_delete=models.CASCADE)
    scheme = models.ForeignKey(AnnotationScheme, null=True, on_delete=models.CASCADE)
    annotator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        )