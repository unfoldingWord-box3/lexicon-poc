from django.urls import path

from .views import (view_entry, 
    demo_entry, list_entries, view_entry_alignment, 
    view_verse, view_cooccurrences, view_collocates,
    view_dictionary, view_parsed_dictionary, 
    view_resources, view_forms,
    )

urlpatterns = [
    path('', list_entries, name='list_entries'),
    path('demo', demo_entry, name='demo_entry'),
    path('lexicon/<str:entry_id>/', view_entry, name='view_entry'),
    path('concordance/<str:main_entry>/<str:sec_entry>/', view_cooccurrences, name='query'),
    path('collocates/<str:lemma>/', view_collocates, name='view_collocates'),
    path('dictionary/<str:entry_id>/', view_dictionary, name='view_dictionary'),
    path('dictionary/<str:entry_id>/parsed', view_parsed_dictionary, name='view_parsed_dictionary'),    
    path('resources/<str:entry_id>/', view_resources, name='view_resources'),
    path('forms/<str:entry_id>/', view_forms, name='view_forms'),
    path('alignment/<str:entry_id>/', view_entry_alignment, name='view_entry_alignment'),
    path('verse/<str:book>/<int:chapter>/<int:verse>/', view_verse, name='view_verse'),
]