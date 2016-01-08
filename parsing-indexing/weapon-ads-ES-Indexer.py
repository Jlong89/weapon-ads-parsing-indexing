'''
	Python script used to index json docs into elasticsearch under json_weapons_index index
'''

import os
import sys
import json
import elasticsearch
import re
reload(sys) 
sys.setdefaultencoding('UTF8')
#from elasticsearch import Elasticsearch
#es = Elasticsearch() #by default it connects to localhost:9200

host = 'localhost:9200'
es = elasticsearch.Elasticsearch(hosts=[{'host': host, 'port': 80}], http_auth=None, use_ssl=False, verify_certs=False, ca_certs=None, client_cert=None, connection_class=elasticsearch.connection.RequestsHttpConnection)

#get file
file_path = sys.argv[1]

doc = {}
#obtain wanted fields from json docs
for aFile in os.listdir(file_path):
	if aFile == '.DS_Store':
		continue
	curFilePath = "{0}/{1}".format(file_path, aFile)
	jsonFile = open(curFilePath, 'r')
	aJson = json.load(jsonFile)

	if "availableAtOrFrom" in aJson and 'address' in aJson["availableAtOrFrom"] and 'name' in aJson["availableAtOrFrom"]['address']:
		location = aJson["availableAtOrFrom"]["address"]["name"]
		doc['location']=location

	if "description" in aJson:
		description = aJson['description']
		doc['description']=description

	if "geonames_address" in aJson and 'geo' in aJson["geonames_address"][0]:
		lat = aJson["geonames_address"][0]["geo"]["lat"]
		lon = aJson["geonames_address"][0]["geo"]["lon"]
		coord = str(lat) +", " + str(lon)
		doc['coord']=coord
		if "fallsWithinState1stDiv" in aJson["geonames_address"][0] and "hasName" in aJson["geonames_address"][0]["fallsWithinState1stDiv"]:
			doc['state']=aJson["geonames_address"][0]["fallsWithinState1stDiv"]["hasName"]["label"]	

	if 'price' in aJson:
		price= str(aJson["price"]) 
		if re.match("^[0-9]*$", price):
			doc['price']=float(price)

	if 'title' in aJson:
		title= aJson["title"]
		doc['title']=title

	if 'publisher' in aJson and 'name' in aJson['publisher']:
		publisherName= aJson['publisher']['name']
		doc['publisherName']=publisherName
	
	if 'seller' in aJson:
		if 'memberOf' in aJson['seller'] and 'startDate' in aJson["seller"]["memberOf"]:
			sellerStartDate=aJson["seller"]["memberOf"]['startDate'].replace('T', ' ')
			orgName=aJson["seller"]["memberOf"]["memberOf"]["name"]
			doc['sellerStartDate']=sellerStartDate
			doc['orgName']=orgName
		if	"description" in aJson["seller"]:
			doc['sellerDesc']=aJson["seller"]["description"]

	if "availabilityStarts" in aJson:
		if len(aJson['availabilityStarts'])!='':
			availableDate=aJson['availabilityStarts'].replace('T', ' ')
			doc['availableDate']=availableDate


	if "url" in aJson:
		postUrl = aJson["url"]
		doc['postUrl']=postUrl

	if "itemOffered" in aJson:
		if 'category' in aJson["itemOffered"]:
			itemCategory=aJson['itemOffered']['category']
			doc['itemCategory']=itemCategory

		if "keywords" in aJson["itemOffered"]:
			itemKeywords=''
			for word in aJson['itemOffered']['keywords']:
				if len(itemKeywords)==0:
					itemKeywords += word
				else:
					itemKeywords += ' '+word
			doc['itemKeywords']=itemKeywords

		if "manufacturer" in aJson["itemOffered"]:
			itemManufacturer = aJson["itemOffered"]["manufacturer"]
			doc['itemManufacturer']=itemManufacturer			

	jsonFile.close()

	fileName = aFile.split('.')[0]

	print 'id: '+fileName
	'''
		post new extracted json to elasticsearch
	'''
	res = es.index(index="json_weapons_index", doc_type='weapon_doc', id=fileName, body=doc)
	print 'Indexing '+ fileName + ' into weapons_index_metadata, indexed: '+str(res['created'])+'.\n'	

print "finished indexing!!!!!!!!!!!!!"








	


	


	
		
