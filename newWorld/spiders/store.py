import requests
import json
import os

url = "https://www.ishopnewworld.co.nz/CommonApi/Store/GetStoreList"
response = requests.post(url)
content = json.loads(response._content)
allStores = content['stores']

for store in allStores:
    id1 = store['id']
    name = store['name']
    latitude = store['latitude']
    longitude = store['longitude']

    if not os.path.exists('store'):
        os.mkdir('store')
    if os.path.exists('store/' + name + '.json'):
        os.remove('store/' + name + '.json')
    f = open('store/' + name + '.json', 'a')
    f.write(json.dumps({'id': id1, 'name': name, 'latitude': latitude, 'longitude': longitude}))
    f.close()


# class test(scrapy.Spider):

#     name = 'test'

#     def start_requests(self):
#         yield scrapy.Request(url = "https://www.newworld.co.nz/BrandsApi/BrandsStore/GetBrandStores", 
#                             callback = self.parse,
#                             method = 'POST')

#     def parse(self, response):
#         allStores = json.loads(response.body)["stores"]
#         for item in allStores:
#             name = item['name']
#             id = item['id']
#             storeId = item['storeId']
        
#             if not os.path.exists('store'):
#                 os.mkdir('store')
#             if os.path.exists('store/' + name + '.json'):
#                 os.remove('store/' + name + '.json')
#             f = open('store/' + name + '.json', 'a')
#             f.write(json.dumps([name, id, storeId]))
#             f.close()