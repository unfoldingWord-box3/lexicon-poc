from django.urls import path

from .views import view_entry, demo_entry, list_entries, view_entry_alignment

urlpatterns = [
    path('', list_entries, name='list_entries'),
    path('demo', demo_entry, name='demo_entry'),
    path('<str:entry_id>/', view_entry, name='view_entry'),
    path('alignment/<str:entry_id>/', view_entry_alignment, name='view_entry_alignment')
]
