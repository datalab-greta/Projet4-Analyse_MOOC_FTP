#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 11:56:55 2019

@author: tarik
"""

import requests, pprint, os

from pymongo import MongoClient # librairie qui va bien
import configparser

config = configparser.ConfigParser()
config.read_file(open(os.path.expanduser("~/.datalab.cnf")))

CNF = "mongoBDD"
BDD = "Datalab"

# Ouverture connection -> mongo sur serveur
client = MongoClient('mongodb://%s:%s@%s/?authSource=%s' % (config[CNF]['user'], config[CNF]['password'], config[CNF]['host'], BDD))
print(client)

bdd = client['MOOC_GRP_FTP'] # BDD "Datalab" de mongoDB sur serveur
bdd
print("'MOOC_GRP_FTP' Collections:")
#~ for cn in bdd.list_collection_names():
    #~ print("-"+cn)
collec = client['MOOC_GRP_FTP']['Test']

base = "https://www.fun-mooc.fr/courses/"
course = "course-v1:ulb+44013+session02"
post = "1101d7b103de2b07eb94055f098217173fe3cafd/threads/5d7f5b4f1c89dcd7d8014bda"

response = requests.get(
    base+course+"/discussion/forum"+post,
    params={'ajax': 1, 'resp_skip': 0, 'resp_limit': 25},
    #headers={'Accept': 'application/vnd.github.v3.text-match+json'},
    headers={
        #"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:69.0) Gecko/20100101 Firefox/69.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        #"Accept-Language": "en-US,en;q=0.5",
        "X-CSRFToken": "sjAhMYoMMTPa4d66Pk685mTb7wog3uQR",
        "X-Requested-With": "XMLHttpRequest",
        #'Referer': 'https://www.fun-mooc.fr/courses/course-v1:MinesTelecom+04026+session05/discussion/forum/204c764cf87424d86a6259562d1d200afe30ab9a/threads/5d9481db1c89dcf269015b6f' ,
        'Cookie': 'csrftoken=sjAhMYoMMTPa4d66Pk685mTb7wog3uQR; sessionid=7n3lb7ui2q1kzbwfsqxqg0qn3bw8nxwl; acceptCookieFun=on; atuserid=%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%2289955914-d4bb-491e-abe7-58c30d9fa62d%22%2C%22options%22%3A%7B%22end%22%3A%222020-11-03T07%3A53%3A13.359Z%22%2C%22path%22%3A%22%2F%22%7D%7D; atidvisitor=%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-602676-%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A15724800%2C%22end%22%3A15724800%7D%7D; edxloggedin=true; edx-user-info="{\"username\": \"Tarik37\"\054 \"version\": 1\054 \"email\": \"tarik.medjahed@gmail.com\"\054 \"header_urls\": {\"learner_profile\": \"https://www.fun-mooc.fr/u/Tarik37\"\054 \"logout\": \"https://www.fun-mooc.fr/logout\"\054 \"account_settings\": \"https://www.fun-mooc.fr/account/settings\"}}"'
    },
)

print(response.content)
pprint.pprint(response.json())

collec.insert_one(response.json())


'''
await fetch("https://www.fun-mooc.fr/courses/MinesTelecom/04017S02/session02/discussion/forum/49a1da04c7cbd68b1f8b8561b3c5859446659c20/threads/589c3f2ba0241e069e002c94?ajax=1&resp_skip=0&resp_limit=25", {
    "credentials": "include",
    "headers": {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:69.0) Gecko/20100101 Firefox/69.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "X-CSRFToken": "gANDlNXv8Fa6TXwa8QNquNQBpMzxGh6g",
        "X-Requested-With": "XMLHttpRequest"
    },
    "referrer": "https://www.fun-mooc.fr/courses/MinesTelecom/04017S02/session02/discussion/forum/49a1da04c7cbd68b1f8b8561b3c5859446659c20/threads/589c3f2ba0241e069e002c94",
    "method": "GET",
    "mode": "cors"
});
curl 'https://www.fun-mooc.fr/courses/MinesTelecom/04017S02/session02/discussion/forum/49a1da04c7cbd68b1f8b8561b3c5859446659c20/threads/589c3f2ba0241e069e002c94?ajax=1&resp_skip=0&resp_limit=25' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:69.0) Gecko/20100101 Firefox/69.0' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'X-CSRFToken: gANDlNXv8Fa6TXwa8QNquNQBpMzxGh6g' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -H 'Referer: https://www.fun-mooc.fr/courses/MinesTelecom/04017S02/session02/discussion/forum/49a1da04c7cbd68b1f8b8561b3c5859446659c20/threads/589c3f2ba0241e069e002c94' -H 'Cookie: defaultRes=2400%2C0; csrftoken=gANDlNXv8Fa6TXwa8QNquNQBpMzxGh6g; __utma=218362510.833297836.1474796751.1542221217.1542232713.415; acceptCookieFun=on; atuserid=%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%2231d3b730-8db4-4c4b-9b98-be9e14c92513%22%2C%22options%22%3A%7B%22end%22%3A%222020-09-27T13%3A54%3A31.376Z%22%2C%22path%22%3A%22%2F%22%7D%7D; atidvisitor=%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-602676-%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A15724800%2C%22end%22%3A15724800%7D%7D; sessionid=uvgks3rokde8k6hspkm3x24le4vm5d6p; edxloggedin=true; edx-user-info="{\"username\": \"EGo41\"\054 \"version\": 1\054 \"email\": \"emmanuel.goudot@gmail.com\"\054 \"header_urls\": {\"learner_profile\": \"https://www.fun-mooc.fr/u/EGo41\"\054 \"logout\": \"https://www.fun-mooc.fr/logout\"\054 \"account_settings\": \"https://www.fun-mooc.fr/account/settings\"}}"'


curl 'https://www.fun-mooc.fr/courses/course-v1:MinesTelecom+04026+session05/discussion/forum/204c764cf87424d86a6259562d1d200afe30ab9a/threads/5d9481db1c89dcf269015b6f?ajax=1&resp_skip=0&resp_limit=25'
-H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:69.0) Gecko/20100101 Firefox/69.0' 
-H 'Accept: application/json, text/javascript, */*; q=0.01' 
-H 'Accept-Language: en-US,en;q=0.5' --compressed 
-H 'X-CSRFToken: LvmImlOzFWNoC8oQbAdPUvlP7a4ab3KZ' 
-H 'X-Requested-With: XMLHttpRequest' 

-H 'Connection: keep-alive' 
-H 'Referer: https://www.fun-mooc.fr/courses/course-v1:MinesTelecom+04026+session05/discussion/forum/204c764cf87424d86a6259562d1d200afe30ab9a/threads/5d9481db1c89dcf269015b6f' 
-H 'Cookie: defaultRes=2400%2C0; csrftoken=LvmImlOzFWNoC8oQbAdPUvlP7a4ab3KZ; __utma=218362510.833297836.1474796751.1542221217.1542232713.415; acceptCookieFun=on; atuserid=%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%2231d3b730-8db4-4c4b-9b98-be9e14c92513%22%2C%22options%22%3A%7B%22end%22%3A%222020-09-27T13%3A54%3A31.376Z%22%2C%22path%22%3A%22%2F%22%7D%7D; atidvisitor=%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-602676-%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A15724800%2C%22end%22%3A15724800%7D%7D; sessionid=kyxq7top4gplpn8dinb5y1ez0wdg6hrl; edxloggedin=true; edx-user-info="{\"username\": \"EGo41\"\054 \"version\": 1\054 \"email\": \"emmanuel.goudot@gmail.com\"\054 \"header_urls\": {\"learner_profile\": \"https://www.fun-mooc.fr/u/EGo41\"\054 \"logout\": \"https://www.fun-mooc.fr/logout\"\054 \"account_settings\": \"https://www.fun-mooc.fr/account/settings\"}}"'


'''