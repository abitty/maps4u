#coding: utf-8

from django.urls import path
from maps.views import map_pages, MapList, MapListPrice,MapDetail,PageDetail,AccList,GravList #,list_by_tag
from . import views

urlpatterns = [
path ('',MapList.as_view()),
#path ('<int:page>',map_pages),
path ('engraving/', GravList.as_view()),
path ('accessory/', AccList.as_view()),
path ('price',MapListPrice.as_view()),
path ('items/<slug:slug>/',MapDetail.as_view()),
path ('page/<slug:slug>/',PageDetail.as_view()),
path ('tags/<tag_id>/', MapList.as_view()),#list_by_tag),
#path ('?s=<search_for>', MapList.as_view()),#list_by_tag),
#path(r'',views.MapListView.as_view()), # список карт
]