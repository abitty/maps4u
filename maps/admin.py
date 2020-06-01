from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline 
from django.utils.safestring import mark_safe
from maps.models import Image, Product, Category, Tag, Page
from django_summernote.admin import SummernoteModelAdmin

from django import forms
from django.db import models


# Register your models here.
class ProductImageInline(admin.TabularInline):
	model = Image
	fields = ['image','order','render']
	readonly_fields = ['render']
	extra=0
	def render(self,obj):
		return mark_safe('<img src="{}" width="64" height="64" />'.format(obj.image.url))
	
class ProductAdmin(SummernoteModelAdmin): #admin.ModelAdmin
	inlines = [
		ProductImageInline,
	]
	prepopulated_fields = {'slug': ('title',)}
	list_display = ['title', 'prod_image', 'partnumber', 'price', 'sold']
	list_filter = ['price', 'sold']
	list_editable = ['partnumber', 'price', 'sold']
	search_fields = ['title','partnumber']
	readonly_fields=['prod_image']
	fields = [('category','tags'),('title','slug','meta_desc','meta_title','meta_h1'),('partnumber','price','sold'),('annotation','epigraph','epigraph_author','year'),('description'),('author','source','material'),('carton','glass'),('mapsize','framesize')]
	summernote_fields = ('description',)
	'''
	formfield_overrides = {
            models.TextField: {'widget': AdminRedactorEditor(redactor_settings={
        'autoformat': True,
		'buttons': ['html', 'format', 'bold', 'italic', 'deleted', 'lists', 'image', 'file', 'link','redo', 'undo', 'underline', 'ol', 'ul', 'indent', 'outdent', 'sup', 'sub'],
		'pastePlainText': True,
        'overlay': False,
    })},
    }
	'''
	def prod_image(self, obj):
		if obj.image() and obj.image().url:
			return mark_safe("<img src='{}'  width='64' height='64' />".format(obj.image().url))
		else:
			return "-"
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