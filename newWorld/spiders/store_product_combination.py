import os
import json
import pandas as pd

# load all data in each branch
# might contains duplicate data
num = 0
json_list = []
file_level_1 = 'store_product'
if os.path.exists(file_level_1):
    # direc_1: store_product
    for direc_1 in os.listdir(file_level_1): 
        # direc_2: branch 
        for direc_2 in os.listdir(file_level_1 + '/' + direc_1):
            # file: category-product for each branch
            for file in os.listdir(file_level_1 + '/' + direc_1 + '/' + direc_2):
                f = open(file_level_1 + '/' + direc_1 + '/' + direc_2 + "/" + file, 'r')
                jsontext = json.loads(f.read())
                for item in jsontext:
                    json_list.append(item)

    if os.path.exists('data_output.json'):
        os.remove('data_output.json')
    f = open('data_output.json', 'a')
    f.write(json.dumps(json_list))
    f.close()

data = pd.read_json('data_output.json')
data.to_csv('data_output.csv')