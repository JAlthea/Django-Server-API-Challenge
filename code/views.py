from django.shortcuts import render
from myapp.item.models import Item, Ingredient
from myapp.item.jsonParser import jsonParser
import json, math
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Setting
baseImageUrl = 'https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/'
thumbnailSize = 'thumbnail/'
fullSize = 'image/'
fileExtension = '.jpg'
itemPerPage = 50

# pk에 해당하는 아이템의 skin_type에 대해서 가장 적합한 3개의 아이템도 같이 반환해야한다. 
# Detail information about choiced 1 item + Recommended 3 items : ordering (skin_type, price)
@api_view(['GET'])
def getItemDetailView(request, pk):
	
	# Append choiced 1 item
	try:
		choiceItem = Item.objects.get(item_id=pk)
	except Item.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	itemList = []
	itemList.append({
			"id": choiceItem.item_id,
			"imgUrl": baseImageUrl + fullSize + choiceItem.imageId + fileExtension,
			"name": choiceItem.name,
			"price": choiceItem.price,
			"gender": choiceItem.gender,
			"category": choiceItem.category,
			"ingredients": choiceItem.ingredients,
			"monthlySales": choiceItem.monthlySales,
		})

	# Append recommended 3 items
	skin_type = request.GET.get('skin_type')	#Essential
	orderedList = [] # QuerySet list
	if skin_type == 'oily':
		orderedList = Item.objects.order_by('-oilyScores', 'price').exclude(item_id__exact=pk)[:3]
	elif skin_type == 'dry':
		orderedList = Item.objects.order_by('-dryScores', 'price').exclude(item_id__exact=pk)[:3]
	else:
		orderedList = Item.objects.order_by('-sensitiveScores', 'price').exclude(item_id__exact=pk)[:3]

	for item in orderedList.iterator():
		itemList.append({
				"id": item.item_id,
				"imgUrl": baseImageUrl + thumbnailSize + item.imageId + fileExtension,
				"name": item.name,
				"price": item.price,
			})

	return Response(itemList)


# Filtered all items information : (skin_type & price), (category), (page), (include_ingredient), (exclude_ingredient)
@api_view(['GET'])
def getItemsListView(request):

	skin_type = request.GET.get('skin_type')	#Essential
	category = request.GET.get('category')		#Optional
	page = request.GET.get('page')				#Optional
	include_ingredient = request.GET.get('include_ingredient')	#Optional
	exclude_ingredient = request.GET.get('exclude_ingredient')	#Optional

	# filtering 'skin_type' (Essential)
	orderedList = []	# QuerySet list
	if skin_type == 'oily':
		orderedList = Item.objects.order_by('-oilyScores', 'price')
	elif skin_type == 'dry':
		orderedList = Item.objects.order_by('-dryScores', 'price')
	else:
		orderedList = Item.objects.order_by('-sensitiveScores', 'price')

	# filtering 'category'
	filteredList = orderedList	# QuerySet list
	if category != None:
		filteredList = orderedList.filter(category=category)

	# filtering 'ingredient'
	bIncludeCheck = False
	bExcludeCheck = False
	interSet = set()
	includeSet = set()
	excludeSet = set()

	# include_ingredient에 있는 성분 모두 있으면, includeSet에 더한다.
	if include_ingredient != None:
		bIncludeCheck = True
		for item in filteredList.iterator():
			count = 0
			for i in item.ingredients.split(','):
				for j in include_ingredient.split(','):
					if i == j:
						count += 1
						break
			if count == len(include_ingredient.split(',')):
				includeSet.add(item)

	# exclude_ingredient에 있는 성분 중에서 하나라도 있으면, excludeSet에 더한다.
	if exclude_ingredient != None:
		bExcludeCheck = True
		for item in filteredList.iterator():
			bCheck = False
			for i in item.ingredients.split(','):
				if bCheck == True:
					break
				for j in exclude_ingredient.split(','):
					if i == j:
						bCheck = True
						break
			if bCheck == False:
				excludeSet.add(item)

	# include_ingredient와 exclude_ingredient의 교집합
	if bIncludeCheck == True and bExcludeCheck == False:
		interSet = interSet.union(includeSet)
	elif bIncludeCheck == False and bExcludeCheck == True:
		interSet = interSet.union(excludeSet)
	elif bIncludeCheck == True and bExcludeCheck == True:
		interSet = interSet.union(includeSet.intersection(excludeSet))
	else:
		interSet = filteredList

	# filtering 'page'
	page = 1 if page == None or int(page) < 1 else int(page)
	max = 0
	if page * itemPerPage > len(interSet):
		page = math.ceil(len(interSet) / itemPerPage)
		max = len(interSet)
	else:
		max = page * itemPerPage
	min = (page - 1) * itemPerPage

	## filtered list ##
	interList = list(interSet)
	itemList = []
	if max != 0:
		for i in range(min, max):
			itemList.append({
					"id": interList[i].item_id,
					"imgUrl": baseImageUrl + thumbnailSize + interList[i].imageId + fileExtension,
					"name": interList[i].name,
					"price": interList[i].price,
					"ingredients": interList[i].ingredients,
					"monthlySales": interList[i].monthlySales,
				})

	return Response(itemList)



# 후에 대체 => seed: python manage.py loaddata myapp/item/fixtures/items-data.json
def initDB(request):
	jsonParser()
	return render(request, 'index.html', { 'contents_text': 'Success : All Data init' })

def printAll(request):
	item_list = []
	for item in Item.objects.all():
		item_list.append({
			"id": item.item_id,
			"imageId": item.imageId,
		    "name": item.name,
		    "price": item.price,
		    "gender": item.gender,
		    "category": item.category,
		    "ingredients": item.ingredients,
		    "monthlySales": item.monthlySales,
		    "oilyScores": item.oilyScores,
		    "dryScores": item.dryScores,
		    "sensitiveScores": item.sensitiveScores, 
		})
	ingredient_list = []
	for ingredient in Ingredient.objects.all():
		ingredient_list.append({
			"name": ingredient.name,
			"oily": ingredient.oily,
		    "dry": ingredient.dry,
		    "sensitive": ingredient.sensitive,
		})
	all_list = item_list + ingredient_list
	return render(request, 'index.html', { 'contents_text': all_list })
