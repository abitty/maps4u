from django.db import models

# Create your models here.
"""
class Carton(models.Model):
	carton = models.CharField("Паспарту", max_length=45,blank=False)
	def __str__(self):
		return self.carton
	def __unicode__(self):
		return self.carton
	class Meta:
		verbose_name = "Паспарту"
		verbose_name_plural = "Паспарту"
		indexes = [
			models.Index(fields=['carton']),
		]	
		
class Frame(models.Model):
	frame = models.CharField("Рама", max_length=45,blank=False)
	def __str__(self):
		return self.frame
	def __unicode__(self):
		return self.frame
	class Meta:
		verbose_name = "Рама"
		verbose_name_plural = "Рамы"
		indexes = [
			models.Index(fields=['frame']),
		]	

class Glass(models.Model):
	glass = models.CharField("Стекло", max_length=45,blank=False)
	def __str__(self):
		return self.glass
	def __unicode__(self):
		return self.glass
	class Meta:
		verbose_name = "Стекло"
		verbose_name_plural = "Стёкла"
		indexes = [
			models.Index(fields=['glass']),
		]	
"""

class Tag(models.Model):
	tag = models.CharField(max_length=128)
	def __str__(self):
		return self.tag
	class Meta:
		verbose_name = "Тэг"
		verbose_name_plural = "Тэги"
        
class Category(models.Model):
	title = models.CharField("Название", max_length=128,blank=False)
	#products = model.ForeignKey(Product,on_delete=models.CASCADE)
	#text = models.TextField("Аннотация",blank=True)
	slug = models.SlugField(allow_unicode=False, unique=True)
	image = models.ImageField("Изображение категории",upload_to = 'uploads/',blank=True)
	meta_desc = models.CharField("meta-description",max_length=63,blank=False,default='')
	meta_title = models.CharField("meta-title",max_length=63,blank=False,default='')
	meta_h1= models.CharField("meta-h1",max_length=63,blank=False,default='')
        
	class Meta:
		verbose_name = "Категория"
		verbose_name_plural = "Категории"
		
	def __str__(self):
		return self.title
	def __unicode__(self):
		return self.title
		


    
class Product(models.Model):
	CARTON_CHOICES = (
		(0,'музейный бархат'),
		(1,'бархат'),
		(2,'лён'),
		(3,'другие виды (рисовая бумага)'),
		(4,'двойное комбинированное'),
		(5,'двойной консервационный картон'),
		(6,'консервационный картон'),
		(7,'двойной лён'),
		)
	GLASS_CHOICES = (
		(0,'безбликовое стекло'),
		(1,'багетное стекло 2 мм'),
	)

	category = models.ForeignKey("Category",on_delete=models.CASCADE)
	tags = models.ManyToManyField(Tag,db_index=True,blank=True)
	#images = models.ForeignKey(Images,on_delete=models.CASCADE)
	slug = models.SlugField(allow_unicode=False,db_index=True)
	title = models.CharField("Название", max_length=250,blank=False,db_index=True)
	partnumber = models.CharField("Артикул", max_length=16,blank=False, db_index=True)
	annotation  = models.TextField("Аннотация", blank=True)
	description = models.TextField("Описание",blank=True)
	year = models.IntegerField("Год",blank=True,null=True)
	epigraph = models.TextField("Эпиграф",blank=True,null=True,default=None)
	epigraph_author = models.CharField("Автор эпиграфа",max_length=250,blank=True,null=True,default=None)
	author = models.CharField("Картограф",max_length=128,blank=True,null=True,default=None)
	material = models.CharField("Техника",max_length=128,blank=True,null=True,default=None)
	source = models.CharField("Источник",max_length=250,blank=True,null=True,default=None)
	carton = models.IntegerField("Паспарту", choices = CARTON_CHOICES, blank=True,null=True,default=None)
	glass = models.IntegerField("Стекло", choices = GLASS_CHOICES, blank=True,null=True,default=None)
	price = models.IntegerField("Цена", db_index=True)
	sold = models.BooleanField("Продано", default = False, db_index=True)
	mapsize = models.CharField("Размер поля карты",max_length=63,blank=True,null=True,default=None)
	framesize = models.CharField("Размер рамы",max_length=63,blank=True,null=True,default=None)
	meta_desc = models.CharField("meta-description",max_length=63,blank=True,null=True,default=None)
	meta_title = models.CharField("meta-title",max_length=63,blank=True,null=True,default=None)
	meta_h1= models.CharField("meta-h1",max_length=63,blank=True,null=True,default=None)
	vertical = models.BooleanField("Вертикально", default=True)

        
	class Meta:
		verbose_name = "Продукт"
		verbose_name_plural = "Продукты"
        
	def __unicode__(self):
		return self.title
	def __str__(self):
		return self.title
		
	def carton_text(self):
		result = None
		for k,v in self.CARTON_CHOICES:
			if k == self.carton:
				result = v
		return result
	def glass_text(self):
		result = None
		for k,v in self.GLASS_CHOICES:
			if k == self.glass:
				result = v
		return result
		
	def image(self):
		try:
			img = Image.objects.filter(product=self).order_by('order').first().image
		except AttributeError:
			img = None
		return img
		
	def geometry(self):
		if self.vertical:
			return "x280"
		else:
			return "280"
	def url(self):
		return "/items/{}".format(self.slug)
		
	def _get_unique_slug(self):
		#slug = slugify(self.title)
		unique_slug = self.slug
		num = 1
		while Product.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(self.slug, num)
			print ("try new slug: ", unique_slug)
			num += 1
		return unique_slug

	def save(self, *args, **kwargs):
		if self.pk is None:
			self.slug = self._get_unique_slug()
		if not self.meta_desc:
			self.meta_desc = self.annotation[:63]
		if not self.meta_h1:
			self.meta_h1 = self.title[:63]
		if not self.meta_title:
			self.meta_title = self.title[:63]
		super().save(*args, **kwargs)		
		
        
class Image(models.Model):
	product = models.ForeignKey(Product,related_name="images",on_delete=models.CASCADE,null=True,blank=True)
	image = models.ImageField("Изображение",upload_to = 'uploads/',blank=True)
	order = models.IntegerField("Порядок", blank = True, null=True,default=10)
	alt = models.CharField("Подпись", max_length=128,blank=True)
	
	def __unicode__(self):
		return self.image.url
	class Meta:
		verbose_name = "Картинка"
		verbose_name_plural = "Картинки"

class Page(models.Model):
	title = models.CharField("Название", max_length=128,blank=False,db_index=True,unique=True)
	slug = models.SlugField(allow_unicode=False,unique=True,db_index=True)
	parent = models.IntegerField("Номер меню", blank = True, null=True,default=0)
	text = models.TextField("HTML",blank=True)
	order = models.IntegerField("Порядок", blank = True, null=True,default=10)
	meta_desc = models.CharField("meta-description",max_length=63,blank=False,default='')
	meta_title = models.CharField("meta-title",max_length=63,blank=False,default='')
	meta_h1= models.CharField("meta-h1",max_length=63,blank=False,default='')
	
	def __unicode__(self):
		return self.title
	def __str__(self):
		return self.title
	
	def url(self):
		return "/page/{}".format(self.slug)
		
	class Meta:
		verbose_name = "Страница"
		verbose_name_plural = "Страницы"
