#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 09:23:05 2019

@author: tarik
"""

import pprint, os
#Library connexion mongo
from pymongo import MongoClient # librairie qui va bien
import configparser

import pandas as pd
#pour manipuler json en dict python
from ast import literal_eval 
import json

#Library dezipage
import zipfile


#Library pour connexion au site
import requests

from bs4 import BeautifulSoup


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

collec = client['MOOC_GRP_FTP']['MoocWeb_Tarik']
print(collec)


######################################################Connexion au site et navigation#########################################

base1="https://www.fun-mooc.fr/"
base2="courses/"
base = base1+base2
course = "course-v1:ulb+44013+session02"
post = "1101d7b103de2b07eb94055f098217173fe3cafd/threads/5d7f5b4f1c89dcd7d8014bda"
params= "?ajax=1&resp_skip=0&resp_limit=25"
params2="%3Fajax%3D1%26resp_skip%3D0%26resp_limit%3D25"


#params="?ajax=1&resp_skip=0&resp_limit=25"
url = base+course+"/discussion/forum/"


urllog=base1+"login?next=/"+base2+course+"/discussion/forum/"

headers = {
        
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:69.0) Gecko/20100101 Firefox/69.0'
          }

with requests.Session() as sess:
    
    
    res = sess.get(urllog, headers= headers)
    #print(res.status_code)
    #print(res.cookies)
    #print(res.content)

    username = "tarik.medjahed@gmail.com"
    password = "Frost3337"
    
    soup = BeautifulSoup(res.content, 'html.parser')
    #print(soup)
    
    
    payload={'email': username,'password': password}
    payload['csrfmiddlewaretoken'] = soup.find("input", {"name": "csrfmiddlewaretoken"})['value']
    
    
    #print(payload)
    
    #print(res.status_code)
    
    urlpost='https://www.fun-mooc.fr/login_ajax'
      
   
    r = sess.post(urlpost,data= payload, headers= {'Accept': '*/*','Referer': urllog, 'Accept-Encoding': 'gzip, deflate, br',
                                                  'Referer': urllog,
                                                  'Connection': 'keep-alive','Content-Length': '104',
                                                  'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                                                  'Host': 'www.fun-mooc.fr'})
    #print(r.content)
    #print(r.status_code)
    #print(r.cookies)
    #print(r.headers)
    
    CSRF= r.cookies.get_dict()['csrftoken']
    print(CSRF)
    
    res = sess.get(url,headers={ "X-CSRFToken": CSRF, "Accept": "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Referer":url,
                                "Upgrade-Insecure-Requests": "1"
                                })
    print(res.status_code)
    
    #Un get pour récupérer les fils de discution
    urlget=base+course+"?ajax=1&page=1&sort_key=date&sort_order=desc"
    
    res = sess.get(url,headers={ "X-CSRFToken": CSRF, "Accept": "application/json, text/javascript, */*; q=0.01","Referer":url,
                                "Upgrade-Insecure-Requests": "1","X-Requested-With": "XMLHttpRequest",
                                })
    print(res.status_code)
    #print(res.content)
    
 
    
        
    courseid= json.loads(res.content)
    #print(courseid)
    
    #################Recuperation d'une liste d'URL de fils de discussion "listeURLdisct"################################
    liste_course=[]
    listeId=[]
    listeURLdisct=[]
    
    for element in courseid['discussion_data']:
        liste_course.append(element['commentable_id'])
        listeId.append(element['id'])
        listeURLdisct.append(base+course+"/discussion/forum/"+element['commentable_id']+"/threads/"+element['id']+params)
        
        #print(element['commentable_id'])   
        #print(element['id']) 
    #print(liste_course)
    #print(listeId)
    ###################################################################################################
    
    #####################Boucle de requêtes Get pour récupérer les json#################################
    
    for urlgetdisct in listeURLdisct:
        u= urlgetdisct.replace(params,'')
        #print(u)
        #print(urlgetdisct)
        res = sess.get(urlgetdisct,headers={ 'X-CSRFToken': CSRF, 'Accept': 'application/json, text/javascript, */*; q=0.01','Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
                                'Connection': 'keep-alive','Referer':u,'X-Requested-With': 'XMLHttpRequest','Accept-Encoding': 'gzip, deflate, br','Host': 'www.fun-mooc.fr'
                                })
        
        #########################ADD content to dict################################
        #mydict.update(res.content)
        print(res.status_code)
        #print(res.headers)
        print("#######################################################")
        print(res.content)
        print(urlgetdisct)
        print("#######################################################")
        Fjson = json.loads(res.content)
        print(type(Fjson))
        collec.insert_one(Fjson)