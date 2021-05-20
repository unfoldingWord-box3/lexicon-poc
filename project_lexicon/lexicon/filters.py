import django_filters

from .models import Notes, Source


class SourceFilter(django_filters.FilterSet):
    target = django_filters.CharFilter(field_name='target__token', lookup_expr='iregex', label='Target contains')
    not_in_target = django_filters.CharFilter(field_name='target__token', lookup_expr='iregex', label='Not in target', exclude=True)
    notes_category = django_filters.CharFilter(field_name='notes__supportreference', lookup_expr='icontains', label='Support reference contains')


    class Meta:
        model = Source
        fields = {
            'id':['exact'],
            'book':['exact'],
            'chapter':['exact'],
            'verse':['exact'],
            'token':['exact'],
            'lemma':['exact'],
            'morph':['exact', 'regex'],
            'strongs_no_prefix':['exact'],
            'has_prefix':['exact'],
            'occ':['exact'],
            'occs':['exact'],
            'strongs_count':['gt', 'lt'],
        }


class NotesFilter(django_filters.FilterSet):
    supportreference = django_filters.AllValuesFilter(
        widget=django_filters.widgets.LinkWidget(), null_label='Uncategorized',)
    
    o = django_filters.OrderingFilter(
        # {model field name: parameter name}
        # fields=(
        #     ('index', 'index'),
        #     ('source__id', 'min'),
        # ),
        fields = 'index min_source'.split(),

        # {field name: human readable label}
        field_labels={
            'index': 'index',
            'min_source': 'Source',
        }
    )

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