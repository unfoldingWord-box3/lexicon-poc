"""project_lexicon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework import routers

from lexicon.urls import urlpatterns as lexicon_urlpatterns
from api import ( SourceViewSet, 
    TargetViewSet, AlignmentViewSet, WordsViewSet, 
    StrongsM2MViewSet, NotesViewSet, LexiconViewSet, 
    GlossesViewSet, QuestionViewSet, BDBViewSet,
    SimpleSourceViewSet,
)
# from api import SimpleVerse

router = routers.DefaultRouter()
router.register(r'simplesource', SimpleSourceViewSet, basename='simplesource')
router.register(r'source', SourceViewSet)
# router.register(r'simple_source', SimpleVerse, basename='verses')
router.register(r'ult', TargetViewSet)
router.register(r'alignment', AlignmentViewSet)
router.register(r'words', WordsViewSet)
router.register(r'strongs', StrongsM2MViewSet)
router.register(r'notes', NotesViewSet)
router.register(r'lexicon', LexiconViewSet)
router.register(r'glosses', GlossesViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'bdb', BDBViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls), name="api"),
]
urlpatterns += lexicon_urlpatterns

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]