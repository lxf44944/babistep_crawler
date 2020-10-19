import scrapy
import json
import os
import time


class store_cookie(scrapy.Spider):

    name = "store_cookie"

    def start_requests(self):
        # request the change of branch    

        cookies = {}
        cookies['SessionCookieIdV2'] = '8fbd6a23b1ba4dcb9a820a38b7a95039'
        cookies['server_nearest_store'] = '{"StoreId":"e42fdd7c-6a4e-48d5-964c-5654fd36992b","UserLat":"43.4715","UserLng":"-80.5454","StoreLat":"-38.011812","StoreLng":"177.275962","IsSuccess":true}'
        headers = {
            'cookie': cookies, 
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
            }  

        if os.path.exists('store'):
            for item in os.listdir('store'):
                f = open('store/' + item, 'r')
                jsontext = json.loads(f.read())
                store_id = jsontext["id"]

                start_url = 'https://www.ishopnewworld.co.nz/CommonApi/Store/ChangeStore?storeId=' + store_id
                yield scrapy.Request(start_url, callback = self.parse1, headers = headers, meta = {'branch': item[:-5], 'store_id': store_id})
                time.sleep(5)
    

    def parse1(self, response):
        set_cookies = response.headers.getlist('Set-Cookie')
        cookies = {}
        for cookie in set_cookies:
            cookie = str(cookie)[2:str(cookie).index(";")]
            hds = cookie.split('=')
            cookies[hds[0]] = hds[1]

        cookies['SessionCookieIdV2'] = '8fbd6a23b1ba4dcb9a820a38b7a95039'
        cookies['server_nearest_store'] = '{"StoreId":"e42fdd7c-6a4e-48d5-964c-5654fd36992b","UserLat":"43.4715","UserLng":"-80.5454","StoreLat":"-38.011812","StoreLng":"177.275962","IsSuccess":true}'
        headers = {
            'cookie': cookies, 
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
            }


        # send the cookie to the main page
        url = 'https://www.ishopnewworld.co.nz'

        yield scrapy.Request(url, callback=self.parse2, headers=headers, 
                            meta = {'branch': response.meta['branch'], 'store_id': response.meta['store_id']})

        print("返回分店 1th: ", cookies['STORE_ID'])

    
    def parse2(self, response):
        set_cookies = response.headers.getlist('Set-Cookie')
        cookies = {}
        for cookie in set_cookies:
            cookie = str(cookie)[2:str(cookie).index(";")]
            hds = cookie.split('=')
            cookies[hds[0]] = hds[1]
        print("返回分店 2nd：", cookies['STORE_ID'])

        # navi_list = 'https://www.ishopnewworld.co.nz/CommonApi/Navigation/MegaMenu?v=2478&storeId='
        # cookies = {}
        # cookies['SessionCookieIdV2'] = '8fbd6a23b1ba4dcb9a820a38b7a95039'
        # cookies['server_nearest_store'] = '{"StoreId":"e42fdd7c-6a4e-48d5-964c-5654fd36992b","UserLat":"43.4715","UserLng":"-80.5454","StoreLat":"-38.011812","StoreLng":"177.275962","IsSuccess":true}'
        # headers = {
        #     'cookie': cookies, 
        #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
        #     }
        
        # branch = response.meta['branch']
        # store_id = response.meta['store_id']
        # yield scrapy.Request(url = navi_list + store_id, callback = self.parse3, 
        #                         headers = headers, method = 'POST',
        #                         meta = {'branch': branch, 'store_id': store_id}
        #         )


    # def parse3(self, response):
    #     Navigation = json.loads(response.text)
    #     branch = response.meta['branch']
    #     store_id = response.meta['store_id']
    #     self.children(Navigation, branch, store_id)


    # def children(self, text, name, store_id):
    #     json_list = text['NavigationList'][0]

    #     if not os.path.exists('store_cookie'):
    #         os.mkdir('store_cookie')

    #     sub_list = []
    #     sub_list.append([store_id])
    #     url_list = []
    #     list_1 = json_list['Children']
    #     for item_1 in list_1:
    #         name_1 = item_1['Name']
    #         itemName_1 = item_1['ItemName']
    #         list_2 = item_1['Children']
    #         for item_2 in list_2:
    #             name_2 = item_2['Name']
    #             itemName_2 = item_2['ItemName']
    #             list_3 = item_2['Children']
    #             for item_3 in list_3:
    #                 name_3 = item_3['Name']
    #                 itemName_3 = item_3['Name']
    #                 url_list.append({
    #                     'URL_1': item_1['URL'],
    #                     'URL_2': item_2['URL'],
    #                     'URL_3': item_3['URL'],
    #                     'level_1': name_1,
    #                     'itemName_1': itemName_1,
    #                     'level_2': name_2,
    #                     'itemName_2': itemName_2,
    #                     'level_3': name_3,
    #                     'itemName_3': itemName_3
    #                 })
    #     sub_list.append(url_list)

    #     if os.path.exists('store_cookie/' + name + '.json'):
    #         os.remove('store_cookie/' + name + '.json')
    #     f = open('store_cookie/' + name + '.json', 'a')
    #     f.write(json.dumps(sub_list))
    #     f.close()