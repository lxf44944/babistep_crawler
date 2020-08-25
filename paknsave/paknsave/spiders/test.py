import time

import scrapy
import os
import json



class TestSpider(scrapy.Spider):
    name = 'test'
    # ------------------请求分店列表------------------
    start_urls = ['https://www.paknsaveonline.co.nz/CommonApi/Store/GetStoreList']

    def parse(self, response):
        """======处理存储分店信息，对各分店商品类别发起请求======"""
        store_list = []
        parent_dir = 'data/'
        stores = response.json()
        for store in stores["stores"]:
            store_list.append({"id": store["id"], "name": store["name"]})
            store_dir = parent_dir + store["name"]
            create_dir(store_dir)
        for store in store_list:
            # -------------请求列表中各分店的商品类别--------------
            categories_url = 'https://www.paknsaveonline.co.nz/CommonApi/Navigation/MegaMenu?v=2478&storeId=' + store["id"]
            yield scrapy.Request(categories_url, callback=self.parse_stores, meta=store)

    def parse_stores(self, response):
        """=====处理存储相应分店商品分类，对各分类商品逐页发起请求====="""
        cat_list = {
            'store_id': response.meta["id"],
            'store_name': response.meta["name"],
            'cats': [],
        }
        # ------------------存储该分店的商品分类------------------
        parent_dir = 'data/' + cat_list['store_name'] + '/'  # data/'store_name'/
        cats = response.json()
        # 一级分类
        for cat1 in cats["NavigationList"][0]["Children"]:
            cat1_dir = parent_dir + cat1["Name"] + '/'
            create_dir(cat1_dir)
            # 二级分类
            cat1["sub_cats"] = []
            for cat2 in cat1["Children"]:
                cat2_dir = cat1_dir + '/' + cat2["Name"] + '/'
                create_dir(cat2_dir)
                cat1["sub_cats"].append({"url": cat2["URL"], "name": cat2["Name"]})
            cat_list["cats"].append({"url": cat1["URL"],
                                     "name": cat1["Name"],
                                     "sub_cats": cat1["sub_cats"],
                                     })
        cookies = {
            'STORE_ID': cat_list["store_id"] + '|false',
            'SessionCookieIdV2': '91b347c3003c4ceb9586b87e8f8dc50b',
            'server_nearest_store':'{"StoreId": "53989945-1a28-481d-a61c-d6f75f760ada", "UserLat": "-37.8139","UserLng": "144.9634", "StoreLat": "-39.05712", "StoreLng": "174.08127","IsSuccess": true}'
        }
        cat_list['cookies'] = cookies
        store_url = 'https://www.paknsaveonline.co.nz/CommonApi/Store/ChangeStore?storeId=' + cat_list['store_id']
        yield scrapy.Request(store_url, callback=self.parse_categories, cookies=cookies, meta=cat_list)

    def parse_categories(self, response):
        # ------------------对该分店各分类商品发起请求------------------
        cat_list = response.meta
        print("正在请求分店：\n分店名称：" + cat_list['store_name'] + "\n分店ID：" + cat_list["store_id"])
        # 读取各分类商品页
        for cat1 in cat_list['cats']:
            for cat2 in cat1["sub_cats"]:
                for page in range (1,51): #页码最大值为50
                    info = {
                        'store_id': cat_list["store_id"],
                        'store_name': cat_list['store_name'],
                        'cat1': cat1["name"],
                        'cat2': cat2["name"],
                        'cat_url': cat2["url"],
                        'page': str(page),
                    }
                    time.sleep(0.5)
                    product_url = 'https://www.paknsaveonline.co.nz/' + cat2['url'] + '?pg=' + str(page)
                    yield scrapy.Request(product_url, callback=self.parse_products, cookies=cat_list['cookies'], meta=info)

    def parse_products(self, response):
        """==================解析页面中商品信息并存储=================="""
        set_cookies = response.headers.getlist('Set-Cookie')
        cookies = {}
        for cookie in set_cookies:
            cookie = str(cookie)[2:str(cookie).index(";")]
            hds = cookie.split('=')
            cookies[hds[0]] = hds[1]
        print("返回分店：", cookies['STORE_ID'])

        # ------------------------解析商品信息------------------------
        products_num = len(response.xpath('/html/body/div[2]/section[3]/div[1]/div/div[1]/div').extract())
        products = []
        product = {}
        for i in range(1, products_num + 1):
            product_info = response.xpath('/html/body/div[2]/section[3]/div[1]/div/div[1]/div[' + str(
                i) + ']/div/div[3]/@data-options').extract_first()
            product["product_id"] = get_info('productId', product_info)
            product["product_name"] = get_info('productName', product_info, 0)
            product["price_mode"] = get_info('PriceMode', product_info, 0)
            product["price_item"] = get_info('PricePerItem', product_info)
            product["url"] = response.xpath(
                '/html/body/div[2]/section[3]/div[1]/div/div[1]/div[' + str(i) + ']/div/a/@href').extract_first()
            product["cat1"] = response.meta["cat1"]
            product["cat2"] = response.meta["cat2"]
            product["cat_url"] = response.meta["cat_url"]
            product["store_name"] = response.meta["store_name"]
            products.append(product)
            product = {}

        # ========================存储商品信息========================
        if products:
            parent_dir = "data/" + response.meta["store_name"] + "/" + response.meta["cat1"] + "/" + response.meta[
                "cat2"] + "/"
            create_dir(parent_dir)
            file_name = response.meta["page"] + ".json"
            create_file(parent_dir, file_name, products)
            print("已存储于以下路径：" + parent_dir + file_name)


def create_file(dir, name, item):
    """存储json对象到本地文件
    Args:
        dir: 文件存储路径
        name: 文件名
        item: 要存储对JSON对象
    """
    if os.path.exists(dir + '/' + name):
        os.remove(dir + '/' + name)

    f = open(dir + '/' + name, 'a')
    f.write(json.dumps(item))
    f.close()


def create_dir(dir):
    """创建一个本地目录
    Args:
        dir: 要创建的路径
    """
    if not os.path.exists(dir):
        os.mkdir(dir)


def get_info(keyword, desc, offset=1):
    """解析返回页面中的商品信息
    Args:
        keyward: 要提取的属性名，如productId
        desc: 页面中待处理的商品描述
        offset: 用于处理不同字段细微格式差别
    """
    # E.g. "productId" : "5046542-KGM-000PNS"  (offset = 1)
    # E.g. "productName": "Produce Banana"     (offset = 0)
    if keyword in desc:
        start = desc.find(keyword) + len(keyword) + len(' : \"') + offset
        end = desc.find('\"', start)
        return desc[start:end]  # Extract 5046542-KGM-000PNS
    else:
        return ''