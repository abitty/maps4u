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
    def __unicode__(self):
        return self.tag
        
class Category(models.Model):
	title = models.CharField("Название", max_length=128,blank=False)
    #products = model.ForeignKey(Product,on_delete=models.CASCADE)
	slug = models.SlugField(allow_unicode=True, unique=True)
	image = models.ImageField("Изображение категории",upload_to = 'uploads/',blank=True)
    
class Product(models.Model):
	CARTON_CHOICES = (
		(0,'музейный картон паспарту'),
		(1,'бархат'),
		(2,'лен'),
		(3,'другие виды (рисовая бумага)'),
		(4,'двойное А (бархат, лен и пр)'),
		(5,'двойное Б (обычный картон)'),
		(6,'обычное одинарное'),
		)
	GLASS_CHOICES = (
		(0,'безбликовое стекло'),
		(1,'обычное стекло'),
	)

	category = models.ForeignKey("Category",on_delete=models.CASCADE)
	tags = models.ManyToManyField(Tag,db_index=True)
	#images = models.ForeignKey(Images,on_delete=models.CASCADE)
	slug = models.SlugField(allow_unicode=True,unique=True)
	title = models.CharField("Название", max_length=128,blank=False,db_index=True)
	partnumber = models.CharField("Артикул", max_length=16,blank=False)
	annotation  = models.CharField("Аннотация", max_length=256,blank=True)
	description = models.TextField("Описание",blank=True)
	carton = models.IntegerField("Паспарту", choices = CARTON_CHOICES, blank=True)
	glass = models.IntegerField("Стекло", choices = CARTON_CHOICES, blank=True)
	price = models.IntegerField("Цена")
	sold = models.BooleanField("Продано", default = False)
	meta_desc = models.CharField("meta-description",max_length=63,blank=False)
	meta_title = models.CharField("meta-title",max_length=63,blank=False)
	meta_h1= models.CharField("meta-title",max_length=63,blank=False)
    
	def __unicode__(self):
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
        
class Image(models.Model):
    product = models.ForeignKey(Product,related_name="images",on_delete=models.CASCADE)
    image = models.ImageField("Изображение",upload_to = 'uploads/',blank=True)
    order = models.IntegerField("Порядок", blank = True)
    def __unicode__(self):
        return self.image.url

	
	