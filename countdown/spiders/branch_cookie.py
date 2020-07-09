import scrapy
import json
import os


class branch_cookie(scrapy.Spider):
    name = "branch_cookie"
    headers = {'X-Requested-With': 'OnlineShopping.WebApp', 'Host': 'shop.countdown.co.nz',
               'content-type': 'application/json'}

    def start_requests(self):
        if os.path.exists('branch'):
            ids = []
            branchs = []
            for file in os.listdir('branch'):
                f = open('branch/' + file, 'r')
                jsontext = f.read()
                jsons = json.loads(jsontext)
                for jsoninfo in jsons:
                    if not jsoninfo['id'] in ids:
                        ids.append(jsoninfo['id'])
                        branchs.append(jsoninfo)
                f.close
            for branch in branchs:
                yield scrapy.Request(url='https://shop.countdown.co.nz/api/v1/fulfilment/my/suburbs/' + str(branch['id']),
                                     callback=self.parse, headers=self.headers,method='PUT')

    def parse(self, response):

        headers = response.headers.getlist('Set-Cookie')
        branch_header = {}
        for header in headers:
            header = str(header)[2:str(header).index(";")]
            hds = header.split('=')
            branch_header[hds[0]] = hds[1]
        brachinfo = json.loads(response.body)
        browses = brachinfo['browse']
        specials = brachinfo['specials']
        name = response._url[response._url.rindex('/') + 1:]
        if not os.path.exists('branch_info'):
            os.mkdir('branch_info')
        if os.path.exists('branch_info/' + name + '.json'):
            os.remove('branch_info/' + name + '.json')
        f = open('branch_info/' + name + '.json', 'a')
        dom = {'item': browses, 'cookies': branch_header,'specials':specials}
        f.write(json.dumps(dom))
        f.close()
