import django_filters

from .models import Notes


class NotesFilter(django_filters.FilterSet):
    supportreference = django_filters.AllValuesFilter(
        widget=django_filters.widgets.LinkWidget(), null_label='Uncategorized',)

    class Meta:
        model = Notes
        fields = {
            'book': ['exact',],
            'chapter': ['exact',],
            'verse': ['exact',],
            'annotation': ['contains'],
            'source__strongs_no_prefix': ['contains'],
            'source__morph': ['regex'],
            'supportreference': ['exact', 'contains'],
        }