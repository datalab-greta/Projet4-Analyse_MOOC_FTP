#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 09:55:15 2019

@author: alflo
"""

import sys, glob, zipfile, json, ast, demjson,os
from demjson import decode
import configparser
from pymongo import MongoClient


config = configparser.ConfigParser()
config.read_file(open(os.path.expanduser("datalab.cnf")))

CNF = "mongo"
BDD = "Datalab"

########## Ouverture connection -> mongo sur serveur##########
client = MongoClient('mongodb://%s:%s@%s/?authSource=%s' % (config[CNF]['user'], config[CNF]['password'], config[CNF]['host'], BDD))
print(client)

bdd = client['Datalab'] # BDD "Datalab" de mongoDB sur serveur
bdd
#print("'Datalab' Collections:")    
collec = client['MOOC_GRP_FTP']['Zip_to_mongo1']


###########dezippage###############

fichier = glob.glob("/home/fabien/Bureau/projet4/fichier_depart/*")
#print(fichier)

for fil in fichier:
    #print("-"+fil)
    zf = zipfile.ZipFile(fil, 'r') # deZIPpage
    print(type(zf))
    #print(zipfile)
    n=0
    for zipName in zf.namelist():
        try:
            txt = zf.read(zipName).decode("utf-8") #fonction transformer zipfile en STR
            print(type(txt))
            x=ast.literal_eval(txt)  #fonction pour transformer str en json
            print(type(x))
            ###ou####
            #x=ast.literal_eval(zf.read(zipName).decode("utf-8"))
        
        
        
        ####pour verifier sur la console###
        
        #flag="userame" in x['content']
        #print(zipName+":"+x['content']['title']+","+str(flag))
       
        
            collec.insert_one(x) 
        except:
            print("#####") 
                  