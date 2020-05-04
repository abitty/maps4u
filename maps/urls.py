#coding: utf-8

from django.urls import path
from maps.views import AllMaps
from . import views

urlpatterns = [
path ('',AllMaps),
#path(r'',views.MapListView.as_view()), # список карт
]