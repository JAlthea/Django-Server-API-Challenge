from django.db import models
from jsonfield import JSONField

# 상품
class Item(models.Model):
	item_id = models.IntegerField(primary_key=True, default=0)
	imageId = models.CharField(max_length=128, default=0)
	name = models.CharField(max_length=128, default="null")
	price = models.IntegerField(default=0)
	gender = models.CharField(max_length=16, default="null")
	category = models.CharField(max_length=32, default="null")
	ingredients = models.CharField(max_length=128, default="null")
	monthlySales = models.IntegerField(default=0)
	oilyScores = models.IntegerField(default=0)
	dryScores = models.IntegerField(default=0)
	sensitiveScores = models.IntegerField(default=0)

	def __str__(self):
		return self.name

	def setting(self, item_id, imageId, name, price, gender, category, ingredients, monthlySales, oilyScores, dryScores, sensitiveScores):
		self.item_id = item_id
		self.imageId = imageId
		self.name = name		
		self.price = price
		self.gender = gender
		self.category = category
		self.ingredients = ingredients
		self.monthlySales = monthlySales
		self.oilyScores = oilyScores
		self.dryScores = dryScores
		self.sensitiveScores = sensitiveScores

# 성분
class Ingredient(models.Model):
	name = models.CharField(primary_key=True, max_length=128, default="null")
	oily = models.IntegerField(default=0)
	dry = models.IntegerField(default=0)
	sensitive = models.IntegerField(default=0)

	def __str__(self):
		return self.name

	def setting(self, name, oily, dry, sensitive):
		self.name = name
		self.oily = oily
		self.dry = dry
		self.sensitive = sensitive
