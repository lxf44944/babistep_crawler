import scrapy
import os
import json

class store_product(scrapy.Spider):
    name = 'store_product'
    cookies = {}
    cookies['SessionCookieIdV2'] = '8fbd6a23b1ba4dcb9a820a38b7a95039' #'96eaae3fb77841cfbbfc4afa9cf4828a'
    cookies['server_nearest_store'] = '{"StoreId":"e42fdd7c-6a4e-48d5-964c-5654fd36992b","UserLat":"43.4715","UserLng":"-80.5454","StoreLat":"-38.011812","StoreLng":"177.275962","IsSuccess":true}'
    # '{"StoreId":"55d4fe03-e82e-44a8-8324-57f3afcf16ba","UserLat":"-37.8139","UserLng":"144.9634","StoreLat":"-39.05782","StoreLng":"174.07774","IsSuccess":true}'
    headers = {
        'cookie': cookies, 
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    }
    
    start_url = 'https://www.ishopnewworld.co.nz'
    next_url = ''
    page = '?ps=50&pg=1'
    branchs = 'Mt Roskill'

    def start_requests(self):        

        if os.path.exists('store_cookie'):
            file = open('store_cookie/' + self.branchs + '.json', 'r')
            jsontext = file.read()
            urls_info = json.loads(jsontext)
            
            for item in urls_info:
                self.next_url = self.start_url + item['URL_3'] + self.page
                name = {'level_1': item['level_1'], 'level_2': item['level_2'], 'level_3': item['level_3']}
                while self.next_url:
                    yield scrapy.Request(url = self.next_url, callback = self.parse, headers=self.headers, meta={'name': name, 'branch': self.branchs})

            print('All pages are finished')


    # def parse2(self, response):
    #     # levels = response.css('meta[charset="UTF-8"]')
    #     # print(levels.text)
    #     # 1. Check the current store
    #     print("(((((((((((((((((((((((((((((")
    #     m = response.css('div[class="js-ribbon m-ribbon"]').css('div::attr(data-options)').extract()
    #     q = json.loads(m[0])
    #     currentStore = q['CurrentStore']
    #     print(currentStore)
    #     print(";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;")

    def parse(self, response):

        file_level_1 = 'store_product'
        file_level_2 = response.meta['branch']

        level_name = response.meta['name']
        file_level_3 = level_name['level_1']
        file_level_4 = level_name['level_2']
        file_level_5 = level_name['level_3']

        all_products_infor = response.css('div[class="js-product-card-footer fs-product-card__footer-container"]').css('div::attr(data-options)').extract()     
        urls_images = response.css('a[class="fs-product-card__details u-color-black u-no-text-decoration u-cursor"]')
        images = urls_images.css('div[class="fs-product-card__product-image"]').css('div::attr(data-src-s)').extract()
        urls = urls_images.css('a::attr(href)').extract()


        for i in range(len(all_products_infor)):
            
            product = []
            item_json = json.loads(all_products_infor[i]) 
            productDetails = item_json['ProductDetails']

            product.append({
                'ProductId': item_json['productId'],
                'ProductName': item_json['productName'],
                'Branch': file_level_2,
                'level_1': file_level_3,
                'level_2': file_level_4,
                'level_3': file_level_5,
                'Image': images[i],
                'ProductUrl': "www.ishopnewworld.co.nz" + urls[i],
                'PricePerItem': productDetails['PricePerItem'],
                'PriceMode':  productDetails['PriceMode'],
                'HasMultiBuyDeal': productDetails['HasMultiBuyDeal'],
                'MultiBuyDeal': productDetails['MultiBuyDeal'],
                'MultiBuyBasePrice': productDetails['MultiBuyBasePrice'],
                'MultiBuyPrice': productDetails['MultiBuyPrice'],
                'MultiBuyQuantity': productDetails['MultiBuyQuantity'],
                'PromoBadgeImageLabel': productDetails['PromoBadgeImageLabel']
            })

            if not os.path.exists(file_level_1):
                os.mkdir(file_level_1)
            if not os.path.exists(file_level_1 + "/" + file_level_2):
                os.mkdir(file_level_1 + "/" + file_level_2)
            if not os.path.exists(file_level_1 + "/" + file_level_2 + "/" + file_level_3):
                os.mkdir(file_level_1 + "/" + file_level_2 + "/" + file_level_3)

            file_path = file_level_1 + '/' + file_level_2 + '/' + file_level_3 + '/' + str(item_json['productId']) + '.json'
            if os.path.exists(file_path):
                os.remove(file_path)
            f = open(file_path, 'a')
            f.write(json.dumps(product))
            f.close()

        try:
            part_url = response.css('a[class="btn btn--primary btn--large fs-pagination__btn fs-pagination__btn--next"]').css('a::attr(href)').extract()
            self.next_url = part_url[0]
        except:
            self.next_url = ''
            print("It is the last page")

