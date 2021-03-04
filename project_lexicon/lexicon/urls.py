from django.urls import path

from .views import view_entry, demo_entry, list_entries, view_entry_alignment, view_verse, query, view_collocates

urlpatterns = [
    path('', list_entries, name='list_entries'),
    path('demo', demo_entry, name='demo_entry'),
    path('lexicon/<str:entry_id>/', view_entry, name='view_entry'),
    path('concordance/<str:main_entry>/<str:sec_entry>/', query, name='query'),
    path('collocates/<str:lemma>/', view_collocates, name='view_collocates'),
    path('alignment/<str:entry_id>/', view_entry_alignment, name='view_entry_alignment'),
    path('verse/<str:book>/<int:chapter>/<int:verse>/', view_verse, name='view_verse'),
]
