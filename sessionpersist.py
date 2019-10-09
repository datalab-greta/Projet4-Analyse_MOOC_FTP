#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 11:22:31 2019

@author: tarik
"""

import requests, pprint, os
from requests.auth import HTTPBasicAuth
import json

from bs4 import BeautifulSoup
base1="https://www.fun-mooc.fr/"
base2="courses/"
base = base1+base2
course = "course-v1:ulb+44013+session02"
post = "1101d7b103de2b07eb94055f098217173fe3cafd/threads/5d7f5b4f1c89dcd7d8014bda"
params= "?ajax=1&resp_skip=0&resp_limit=25"
params2="%3Fajax%3D1%26resp_skip%3D0%26resp_limit%3D25"


#params="?ajax=1&resp_skip=0&resp_limit=25"
url = base+course+"/discussion/forum/"+post+params


urllog=base1+"login?next=/"+base2+course+post+params2

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
  
    
    
    
    
    res = sess.get(url,headers={ "X-CSRFToken": CSRF, "Accept": "application/json, text/javascript, */*; q=0.01","Referer":url,
                                "Upgrade-Insecure-Requests": "1","X-Requested-With": "XMLHttpRequest",
                                })
    print(res.status_code)
    #print(res.headers)
    print(res.content)
    print(url)
    
