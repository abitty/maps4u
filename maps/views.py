from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from maps.models import Product, Image, Page

# Create your views here.
def AllMaps(request):
    return HttpResponse("Коллекция старинных карт")
	
class MapList(ListView):
	model = Product
	paginate_by = 20
	context_object_name = 'maps'
	template_name='map_list.html'
	def get_queryset(self):
		#mp = Product.objects.filter(sold=False).order_by("title")
		mp = Product.objects.select_related('category').filter(sold=False,category=4).order_by("title")
		
		res=[]
		for m in mp:
			item = {}
			images = []
			item['map']= m
			item['image'] = m.image()
			item['category'] = m.category
			res.append(item)
		
		return res
		
class MapDetail(DetailView):
	model = Product
	context_object_name = 'map'
	template_name='map_detail.html'
	
	def get_context_data(self, **kwargs):
		res = super().get_context_data(**kwargs)
		res['images'] = Image.objects.select_related().filter(product=self.object).order_by('order')
		return res

class GravList(ListView):
	model = Product
	paginate_by = 20
	context_object_name = 'maps'
	template_name='map_list.html'
	def get_queryset(self):
		#mp = Product.objects.filter(sold=False).order_by("title")
		mp = Product.objects.select_related('category').filter(sold=False,category=5).order_by("title")
		
		res=[]
		for m in mp:
			item = {}
			images = []
			item['map']= m
			item['image'] = m.image()
			item['category'] = m.category
			res.append(item)
		
		return res

class AccList(ListView):
	model = Product
	paginate_by = 20
	context_object_name = 'maps'
	template_name='map_list.html'
	def get_queryset(self):
		#mp = Product.objects.filter(sold=False).order_by("title")
		mp = Product.objects.select_related('category').filter(sold=False,category=5).order_by("title")
		
		res=[]
		for m in mp:
			item = {}
			images = []
			item['map']= m
			item['image'] = m.image()
			item['category'] = m.category
			res.append(item)
		
		return res
		
class PageDetail(DetailView):
	model = Page
	context_object_name = 'page'
	template_name='page_detail.html'
	
class PageList(ListView):
	model = Page
	context_object_name = 'pages'
	template_name='page_list.html'
	def get_queryset(self):
		return Page.objects.values('title').order_by('order')
	
class MapListPrice(MapList):
	def get_queryset(self):
		mp = Product.objects.all().order_by("price")
		res=[]
		item = {}
		images=[]
		for m in mp:
			images = []
			item['map']= m
			print("id=",m.id," title=",m.title)
			images = Image.objects.filter(id=m.id)
			#images = Image.objects.all()
			print("len images=",len(images))
			for i in images:
				print ("image url=",i.url)
			item['images'] = images
			res.append(item)
			print('title: ',m.title, 'url: ',m.id)
		return res
	