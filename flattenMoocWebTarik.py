#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 15:52:03 2019

@author: tarik
"""



import pprint, os
#Library connexion mongo
from pymongo import MongoClient # librairie qui va bien
import configparser

import pandas as pd
import numpy as np
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



out={}
def convert(f):
  def flatten(x, name=None):
    if type(x) is dict:
      for a in x:
        val = '.'.join((name, a)) if name else a
        flatten(x[a], val)
    elif type(x) is list:
      for (i, a) in enumerate(x):
        flatten(a, name + f'[{str(i)}]')
    else:
      out[name] = x if x else ""
  flatten(f)
  return out



doc=[]
for document in collec.find():
    doc.append(document)
    #pprint.pprint (document)
    a=convert(document)
    doc.append(a)
    #print(a)



df=pd.DataFrame.from_dict(a, orient='index',columns=['Value'])
print(df)
        

    

df2=df.rename_axis('path').reset_index()
df2.insert(loc=1, column='Subject', value=['' for i in range(df.shape[0])])
df2


df2['Subject'] = [x.rsplit(".", 1)[-1] for x in df2['path']]

print (df2)
df2=df2[df2['Subject'].isin(['username', 'courseware_title', 'updated_at','_id','context','created_at','id','body','comments_count','title','course_id','commentable_id','courseware_url','type'])]
df2
df3=pd.DataFrame.pivot(df2, index = "path", 
                    columns = "Subject")

df3