from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline 
from django.utils.safestring import mark_safe
from maps.models import Image, Product, Category, Tag, Page

# Register your models here.
class ProductImageInline(admin.TabularInline):
	model = Image
	fields = ['image','order','render']
	readonly_fields = ['render']
	extra=0
	def render(self,obj):
		return mark_safe('<img src="{}" width="64" height="64" />'.format(obj.image.url))
	
    
class ProductAdmin(admin.ModelAdmin):
	inlines = [
		ProductImageInline,
	]
	prepopulated_fields = {'slug': ('title',)}
	list_display = ['title', 'prod_image', 'partnumber', 'price', 'sold']
	list_filter = ['price', 'sold']
	list_editable = ['partnumber', 'price', 'sold']
	search_fields = ['title','partnumber']
	readonly_fields=['prod_image']
	fields = [('category','tags'),('title','slug'),('partnumber','price','sold'),('epigraph','epigraph_author','year'),('annotation','description'),('author','material','source','carton','glass'),('meta_desc','meta_title','meta_h1')]
	
	def prod_image(self, obj):
		if obj.image() and obj.image().url:
			return mark_safe("<img src='{}'  width='64' height='64' />".format(obj.image().url))
		else:
			return "-"
	#prod_image.allow_tags = True
	prod_image.short_description = 'Картинка'
	def save_model(self, request, obj, form, change):
		super().save_model(request, obj, form, change)
		try:
			im = obj.image()
			if im:
				obj.vertical = im.height>=im.width
		except AttributeError:
			pass
		super().save_model(request, obj, form, change)
        
class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}

class TagAdmin(admin.ModelAdmin):
	pass

class ImageAdmin(admin.ModelAdmin):
	list_display = ['url', 'prod_owner','prod_image',]	
	def url(self,obj):
		if obj.image:
			return obj.image.url
		else:
			return "файл не выбран"
	def prod_image(self,obj):
		try:
			return mark_safe("<img src='{}'  width='64' height='64' />".format(obj.image.url))
		except ValueError:
			return "-"
	def prod_owner(self,obj):
		if obj.product:
			return obj.product.title
		else:	
			return "-"
	
class PageAdmin(admin.ModelAdmin):	
	prepopulated_fields = {'slug': 'title',}
	list_display = ['title', 'order']
	list_editable = ['order']
	prepopulated_fields = {'meta_desc': ('title',),'meta_title':('title',),'meta_h1':('title',),}

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Image, ImageAdmin)