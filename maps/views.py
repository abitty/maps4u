from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from maps.models import Product, Image, Page, Category
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
def map_pages(request,page):
	mp = Product.objects.select_related('category').filter(sold=False,category=4).order_by("title")
	
	res=[]
	for m in mp:
		item = {}
		images = []
		item['map']= m
		item['image'] = m.image()
		item['category'] = m.category
		res.append(item)
	
		paginator = Paginator(res, 10)
		print ("map_pages")
	return res
'''		
def list_by_tag(request, tag_id):
	mp = Product.objects.filter(tags__id__exact=tag_id)
	res=[]
	print ("list_by_tag")
	print ("len=",len(mp))
	for m in mp:
		item = {}
		item['map']= m
		item['image'] = m.image()
		item['category'] = m.category
		res.append(item)
	
	paginator = Paginator(res, 2)
	return render(request, 'map_list.html', {'object_list': res})
'''
	
class MapList(ListView):
	#model = Product
	paginate_by = 10
	cat_id=4
	context_object_name = 'maps'
	template_name='map_list.html'
	def get_queryset(self, **kwargs):
		#mp = Product.objects.filter(sold=False).order_by("title")
		try:
			tag_id = self.kwargs['tag_id']
			mp = Product.objects.filter(tags__id__exact=tag_id).order_by("year")
		except KeyError:
			search_for=self.request.GET.get("q", "")
			print (self.request)
			if search_for != "":
				search_res = Q(title__icontains=search_for) | Q(partnumber__icontains=search_for)
				mp = Product.objects.select_related('category').filter(search_res).order_by("year")
			else:
				if not self.cat_id is None:
					mp = Product.objects.select_related('category').filter(sold=False,category=self.cat_id).order_by("year")
				else:
					mp = Product.objects.filter(sold=True).order_by("year")
		
		res=[]
		for m in mp:
			item = {}
			images = []
			item['map']= m
			item['image'] = m.image()
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
		
class GravList(MapList):
	cat_id=5
	template_name='gr_list.html'

class AccList(MapList):
	cat_id=6
	template_name='acc_list.html'
	
class ArchList(MapList):
	cat_id=None
	
		
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
	