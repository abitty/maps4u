from django.contrib.sitemaps import Sitemap
from .models import Category, Product, Page, Image

class ProductSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0

    def items(self):
        return Product.objects.all()

    def location(self, obj):
        return '/items/{}'.format(obj.slug)

class PagesSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.8
    def items(self):
        return Page.objects.all()

    def location(self, obj):
        return '/page/{}'.format(obj.slug)
