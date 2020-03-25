import json
from myapp.item.models import Item, Ingredient

class jsonParser:
	def __init__(self):
		with open('C:/users/Jangyongmin/Django/django-template-master/myapp/item/fixtures/ingredients-list.json', 'r', encoding='utf8') as json_file:
			json_dic = json.load(json_file)
			for json_data in json_dic:
				name = json_data["name"]

				# Numbering for skin_type
				oily = json_data["oily"]
				if oily != None:
					oily = 1 if oily == 'O' else -1
				else:
					oily = 0
				dry = json_data["dry"]
				if dry != None:
					dry = 1 if dry == 'O' else -1
				else:
					dry = 0
				sensitive = json_data["sensitive"]
				if sensitive != None:
					sensitive = 1 if sensitive == 'O' else -1
				else:
					sensitive = 0

				nowIngredient = Ingredient()
				nowIngredient.setting(name, oily, dry, sensitive)
				nowIngredient.save()

		with open('C:/users/Jangyongmin/Django/django-template-master/myapp/item/fixtures/items-list.json', 'r', encoding='utf8') as json_file:
			json_dic = json.load(json_file)
			for json_data in json_dic:
				Id = json_data["id"]
				imageId = json_data["imageId"]
				name = json_data["name"]
				price = json_data["price"]
				gender = json_data["gender"]
				category = json_data["category"]
				ingredients = json_data["ingredients"]
				monthlySales = json_data["monthlySales"]
				oilyScore = 0
				dryScore = 0
				sensitiveScore = 0

				# Score for skin_type
				for ingredient_name in ingredients.split(','):
					now_ingredient = Ingredient.objects.get(name=ingredient_name)
					oilyScore += now_ingredient.oily
					dryScore += now_ingredient.dry
					sensitiveScore += now_ingredient.sensitive

				nowItem = Item()
				nowItem.setting(Id, imageId, name, price, gender, category, ingredients, monthlySales, oilyScore, dryScore, sensitiveScore)
				nowItem.save()
