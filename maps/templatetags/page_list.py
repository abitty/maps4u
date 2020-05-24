from django import template
from maps.models import Page

register = template.Library()

@register.inclusion_tag('page_list.html')
def pages(page):
	items = Page.objects.all().order_by('order') 
	return {'items': items}