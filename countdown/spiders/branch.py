import scrapy
import json
import os


class branch(scrapy.Spider):
    name = "branch"
    headers = {'X-Requested-With': 'OnlineShopping.WebApp', 'Host': 'shop.countdown.co.nz',
               'content-type': 'application/json'}
    def start_requests(self):
        branch_names = [
            # 'bi',
            # 'ca',
            # 'dc'
            'Brownsbay',
            'Orewa',
            'Whangaparaoa',
            'Warkworth',
            'Silverdale',
            'Helensville',
            'Mairangi Bay',
            'Sunnynook',
            'Milford',
            'Glenfield',
            'Hauraki',
            'Northcote',
            'Birkenhead',
            'Te Atatu',
            'Henderson',
            'Te Atatu South',
            'Glen Eden',
            'Great North Road',
            'Blockhouse Bay',
            'Lynfield',
            'Mount Roskill',
            'Point Chevalier Road',
            'Grey Lynn',
            'Mount Eden',
            'New Market',
            'Auckland City',
            'Ponsonby',
            'Mount Albert',
            'Greenlane',
            'Meadowbank',
            'St Johns',
            'Three Kings',
            'Onehunga',
            'Mount Wellington',
            'Pakuranga',
            'Botany',
            'Highland Park',
            'Howick',
            'Favona',
            'Mangere',
            'Papatoetoe',
            'Manukau',
            'Manurewa',
            'Beachlands',
            'Takanini',
            'Papakura'
        ]

        # return [scrapy.Request(url=urls[0],  headers=headers)]
        for branch_name in branch_names:
            yield scrapy.Request(url = 'https://shop.countdown.co.nz/api/v1/suburbs?query=' + branch_name,callback=self.parse, headers=self.headers)
    def parse(self, response):
        branchs = json.loads(response.body)['suburbResults']
        name = response._url[response._url.rindex('=') + 1 :]
        if not os.path.exists('branch'):
            os.mkdir('branch')
        if os.path.exists('branch/' + name + '.json'):
            os.remove('branch/' + name + '.json')
        f = open('branch/' + name + '.json', 'a')
        f.write(json.dumps(branchs))
        f.close()
