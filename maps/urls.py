#coding: utf-8

from django.urls import path
from maps.views import AllMaps, MapList, MapListPrice,MapDetail,PageDetail,AccList,GravList
from . import views

urlpatterns = [
path ('',MapList.as_view()),
path ('engraving/', GravList.as_view()),
path ('accessory/', AccList.as_view()),
path ('price',MapListPrice.as_view()),
path ('items/<slug:slug>/',MapDetail.as_view()),
path ('page/<slug:slug>/',PageDetail.as_view()),
#path ('tag/<id>/',PageDetail.as_view()),
#path(r'',views.MapListView.as_view()), # список карт
]