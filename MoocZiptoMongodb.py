#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 10:15:32 2019

@author: tarik
"""

import pprint, os
from pymongo import MongoClient # librairie qui va bien
import configparser

import pandas as pd
from ast import literal_eval
import zipfile
import lzma
from pyunpack import Archive


import json

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

collec = client['MOOC_GRP_FTP']['MoocZip_Tarik']
print(collec)



rootdir = '/home/tarik/Documents/Projet4_machine learning/Documents_json/'
extension = ".zip"

#for subdir, dirs, list_zip in os.walk(rootdir):
#    for file in list_zip:
#        if file.endswith(".zip"):
#            #print(file)
#            name=file.replace('.zip','').replace('.gz','').replace('.7z','')
#            #print(name)
#            #zipfile.ZipFile.extract(file, path=rootdir+name, pwd=None)
#            #print(rootdir+name)
#            z = zipfile.ZipFile(str(rootdir+file), 'r')
#            z.extractall(path=str(rootdir+name))
#            z.close() 
#        elif file.endswith(".gz"):
#            Archive(str(rootdir+file)).extractall(str(rootdir+name))
#
#        elif file.endswith(".7z"):
#            with lzma.open(str(rootdir+file)) as f:
#                f.extractall(str(rootdir+name))
#            
#        else:
#            pass
            
for subdir, dirs, list_file in os.walk(rootdir):
            
        
    for file in list_file:
        
        with open(os.path.join(subdir, file),'r',encoding="utf8") as f:
            #print(file)
            try:   
                content= f.read()
                #Fjson = json.dumps(f)
                
                #convert into JSON:
                #Fjson = json.loads(content)
                #print(Fjson)
                python_dict = literal_eval(content)
                print(type(python_dict))
                collec.insert_one(python_dict)
            except:

                pass
                                  
                        
print(collec)

                    


                    