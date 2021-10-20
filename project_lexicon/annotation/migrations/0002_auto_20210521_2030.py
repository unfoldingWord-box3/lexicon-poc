# Generated by Django 3.1.3 on 2021-05-21 20:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('annotation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotationscheme',
            name='annotators',
            field=models.ManyToManyField(related_name='annotators', to=settings.AUTH_USER_MODEL),
        ),
    ]