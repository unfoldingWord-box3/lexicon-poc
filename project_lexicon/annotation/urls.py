from django.conf.urls import url
from django.urls import path

from .views import ( AnnotationSchemeIndex, 
    AnnotationLabelIndex, CreateAnnotationScheme, CreateAnnotationLabel,
    ViewAnnotationScheme, add_labels_to_scheme,
    AnnotationSourceListView, AnnotationNavigateSource, create_annotation,
)

urlpatterns = [
    url(r'annotation/$', AnnotationSchemeIndex.as_view(), name='list_schemes'),
    url(r'annotation/labels/$', AnnotationLabelIndex.as_view(), name='label_index'),
    url(r'annotation/newscheme/$', CreateAnnotationScheme.as_view(), name='create_scheme'),
    url(r'annotation/newlabel/$', CreateAnnotationLabel.as_view(), name='label_create'),
    path('annotation/scheme/<int:pk>/', ViewAnnotationScheme.as_view(), name='view_scheme'),
    path('annotation/scheme/<int:scheme_id>/labels', add_labels_to_scheme, name='add_labels_to_scheme'),
    path('annotation/scheme/<int:scheme_id>/search', AnnotationSourceListView.as_view(), name='annotate_list_source'),
    path('annotation/scheme/<int:scheme_id>/search/nav', AnnotationNavigateSource.as_view(), name='annotate_nav_source'),
    url(r'ajax/newannotation$', create_annotation, name='create_annotation'),
    # url(r'gist/$', views.gist_scheme, name='gist_scheme'),
]