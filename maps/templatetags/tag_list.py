from django import template
from maps.models import Tag

register = template.Library()

@register.inclusion_tag('tag_list.html')
def tags(page):
	items = Tag.objects.all().order_by('tag')
	return {'items': items}