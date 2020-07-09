import scrapy
import json
import os

class products(scrapy.Spider):
    name = "products"
    def start_requests(self):
        domList = []
        if os.path.exists('branch_info'):
            for file in os.listdir('branch_info'):
                f = open('branch_info/' + file, 'r')
                jsontext = f.read()
                f.close()
                category = json.loads(jsontext)
                cookie = category['cookies']
                specials = category['specials']
                cookieStr = ''
                for key in cookie:
                    cookieStr = cookieStr + key + '=' + cookie[key] + ';'

                items = category['item']
                for item in items:
                    url = item['url']
                    label = item['label']
                    headers = {'X-Requested-With': 'OnlineShopping.WebApp', 'Host': 'shop.countdown.co.nz',
                               'content-type': 'application/json','cookie' : cookieStr}
                    url = 'https://shop.countdown.co.nz/api/v1/products?dasFilter=Department%3B%3B'+url+'%3Bfalse&nextUI=true&target=browse'
                    domList.append({'url':url,'cookie':cookie,'name':file,'page':1, 'label': label,'header' : headers,'status':'browse'})
                for item in specials:
                    url = item['url']
                    label = item['label']
                    headers = {'X-Requested-With': 'OnlineShopping.WebApp', 'Host': 'shop.countdown.co.nz',
                               'content-type': 'application/json','cookie' : cookieStr}
                    url = 'https://shop.countdown.co.nz/api/v1/products?dasFilter=Department%3B%3B'+url+'%3Bfalse&nextUI=true&target=specials'
                    domList.append({'url':url,'cookie':cookie,'name':file,'page':1, 'label': label,'header' : headers,'status':'specials'})
            for dom in domList:
                yield scrapy.Request(url=dom['url'], callback=self.parse1, headers=dom['header'], cookies=dom['cookie'],
                                     meta={'dom': dom}, dont_filter=True)
    def parse1(self,response):
        dom = response.meta['dom']
        products = json.loads(response.body)
        currentPageSize = products['currentPageSize']
        print()
        for i in range(1,currentPageSize + 1):
        # for i in range(1,2):
            dom['page'] = i
            ddd = {'dom':{'url':dom['url'],'cookie':dom['cookie'],'name':dom['name'],'page':i, 'label': dom['label'],'header':dom['header'],'status':dom['status']}}
            yield scrapy.Request(url=dom['url'] + "&page=" + str(i), callback=self.parse2, headers=dom['header'],
                                 meta=ddd, dont_filter=True, cookies=dom['cookie'])

    def parse2(self, response):
        dom = response.meta['dom']
        products = json.loads(response.body)
        p = products['products']['items']

        # print(products['context']['fulfilment']['address'])
        # for product in products['products']['items']:
        #     sku = product['sku']
        #     dom['sku'] = sku
        #     yield scrapy.Request(url= 'https://shop.countdown.co.nz/api/v1/products/' + sku, callback=self.parse3,  cookies=dom['cookie'],headers=dom['header'],meta = {"dom":dom}, dont_filter=True)
        leibie = ''
        for lb in products['breadcrumb']:
            try:
                leibie = leibie + dom['status'] + ', ' + products['breadcrumb'][lb]['name']
            except Exception as e:
                leibie += ''
        fdName = products['context']['fulfilment']['address']
        parentFiles = 'product/'
        if not os.path.exists(parentFiles):
            os.mkdir(parentFiles)
        parentFiles = parentFiles + '/' + fdName
        if not os.path.exists(parentFiles):
            os.mkdir(parentFiles)
        parentFiles = parentFiles + '/' + dom['status']
        if not os.path.exists(parentFiles):
            os.mkdir(parentFiles)
        parentFiles = parentFiles + '/' + dom['label']
        if not os.path.exists(parentFiles):
            os.mkdir(parentFiles)

        if os.path.exists(parentFiles + '/' + str(dom['page']) + '.json'):
            os.remove(parentFiles + '/' + str(dom['page']) + '.json')
        p1 = []

        for product in p:
            p1.append({

                'name': product['name'],
                'price': product['price']['salePrice'],
                'fdName': fdName,
                'leibie': dom['status'],
                'cat': dom['label'],
                'images': product['images']['big'],
                'info': 'https://shop.countdown.co.nz/api/v1/products' + product['sku'],
                'url': 'https://shop.countdown.co.nz/shop/productdetails?stockcode=' + product['sku']

            })
        f = open(parentFiles + '/' + str(dom['page']) + '.json', 'a')
        f.write(json.dumps(p1))
        f.close()
