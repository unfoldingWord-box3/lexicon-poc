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
from rest_framework import routers

from lexicon.urls import urlpatterns as lexicon_urlpatterns
from api import SourceViewSet, TargetViewSet, AlignmentViewSet, TwViewSet, StrongsM2MViewSet

router = routers.DefaultRouter()
router.register(r'source', SourceViewSet)
router.register(r'ult', TargetViewSet)
router.register(r'alignment', AlignmentViewSet)
router.register(r'tw', TwViewSet)
router.register(r'strongs', StrongsM2MViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
urlpatterns += lexicon_urlpatterns