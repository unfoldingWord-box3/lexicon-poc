from django.urls import path

from .views import view_entry, demo_entry

urlpatterns = [
    path('', view_entry),
    path('demo', demo_entry),
]
