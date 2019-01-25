from django.shortcuts import render
import datetime
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from items.models import Item
from django.db import connection

def group_changelog(rows):
	item_arr = []
	changelog_arr = {}
	#print(rows)

	for i in range(1, len(rows)):
		print(changelog_arr)
		row = rows[i]
		item_id = str(row[1])
		attr = row[3]
		if item_id not in item_arr:
			item_arr.append(item_id)
			changelog_arr[item_id] = []
			changelog_arr[item_id].append(attr)
		else:
			changelog_arr[item_id].append(attr)
	return changelog_arr

def get_pretty_notif(rows):
	# TBD 
	notif = []
	for x in rows:
		notif_part = ''
		notif_string =  'For item id '+x+' these attributes were changed: '
		for l in rows[x]:
			notif_part = notif_part + l + ' '
		notif.append(notif_string+notif_part)
	return notif

@csrf_exempt
def changelog(request):
	body = json.loads( request.body.decode('utf-8') )

	ll = """ select 'changetype', 'item_id', 'variant_id', 'attribute', 'variant_id', 'property_id', 'old_value', 'new_value', 'user', 'created_at' union select 'item', item_id, null, attribute, variant_id, null, old_value, new_value, user, created_at  from items_itemchangelog where user='"""+body['user']+"""' and created_at between '"""+body['fromTime']+"""' and '"""+body['toTime']+"""' union select 'variant', item_id, variant_id, attribute, null, property_id, old_value, new_value, user, created_at from items_variantchangelog where user='"""+body['user']+"""' and created_at between '"""+body['fromTime']+"""' and '"""+body['toTime']+"""' """
	cursor = connection.cursor()
	cursor.execute(ll)
	rows = cursor.fetchall()

	response = {
		"notifications": get_pretty_notif( group_changelog(rows) )
	}
	return HttpResponse(json.dumps(response))
