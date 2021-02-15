from django.urls import path

from .views import alt_view_entry, view_entry, demo_entry, list_entries, view_entry_alignment, view_verse

urlpatterns = [
    path('', list_entries, name='list_entries'),
    path('demo', demo_entry, name='demo_entry'),
    path('lexicon/<str:entry_id>/', view_entry, name='view_entry'),
    path('altlexicon/<str:entry_id>/', alt_view_entry, name='alt_view_entry'),
    path('alignment/<str:entry_id>/', view_entry_alignment, name='view_entry_alignment'),
    path('verse/<str:book>/<int:chapter>/<int:verse>/', view_verse, name='view_verse'),
]
