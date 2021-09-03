#coding: utf-8

from django.urls import path, re_path
from maps.views import map_pages, MapList, MapListPrice,MapDetail,PageDetail,AccList,GravList,ArchList #,list_by_tag
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
path ('',MapList.as_view()),
path ('engraving/', GravList.as_view()),
path ('accessory/', AccList.as_view()),
path ('archive/', ArchList.as_view()),
path ('price', MapListPrice.as_view()),
path ('items/<slug:slug>/',MapDetail.as_view()),
path ('page/<slug:slug>/',PageDetail.as_view()),
path ('tags/<tag_id>/', MapList.as_view()),#list_by_tag),
#path ('search/?q=<str:value>', MapList.as_view()),#list_by_tag),
#path(r'',views.MapListView.as_view()), # список карт
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
