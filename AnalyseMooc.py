#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 09:57:40 2019

@author: tarik
"""





import pandas as pd
from ast import literal_eval
import json
import os


#list_file= os.listdir('/home/tarik/Documents/Projet4_machine learning/Documents_json/course-v1_CNAM+01032+session01')
#path= '/home/tarik/Documents/Projet4_machine learning/Documents_json/course-v1_CNAM+01032+session01'


list_id=[]
list_username=[]
list_threadtype=[]
list_courseware_title=[]
#dict_username={}
rootdir = '/home/tarik/Documents/Projet4_machine learning/Documents_json/'

for subdir, dirs, list_file in os.walk(rootdir):


    for file in list_file:
        #print (os.path.join(subdir, file))
    
# Definition du chemin de fichier
        with open(os.path.join(subdir, file),encoding="utf8") as f:
            try:
                content= f.read()
                #print(content)

                # convert into JSON:
                Fjson = json.dumps(content)
                #print(Fjson)
                python_dict = literal_eval(content)
                #print(python_dict)
                _id= python_dict['_id']
                username= python_dict['content']['username']
                courseware_title= python_dict['content']['courseware_title']
                thread_type= python_dict['content']['thread_type']
                #print(username)
                list_id.append(_id)
                list_username.append(username)
                list_courseware_title.append(courseware_title)
                list_threadtype.append(thread_type)
                #dict_username[file] = username
            except:
                list_id.append('undefined')
                list_username.append('undefined')
                list_courseware_title.append('undefined')
                list_threadtype.append('undefined')
                #dict_username[file] = 'undefined'        

pd.set_option("display.colheader_justify","right")
df = pd.DataFrame({"id":list_id,"username":list_username,"nom_du_cours":list_courseware_title,
                   "thread_type":list_threadtype})

print(df)
#Librairie pour compter
import collections
comptage_tout = collections.Counter(list_username)# Compte TOUT 
comptage_top = collections.Counter(list_username).most_common(20)# Compte les 20 premiers
print(comptage_tout)
print('###########################')
print(comptage_top)

# HISTROGRAMME DES 20 USERNAME LES PLUS UTILISE
import matplotlib.pyplot as plt
fig = plt.figure(1, figsize=(30, 20))
plt.bar(*zip(*comptage_top))
plt.title('Top 20 des username')
plt.xlabel('Quantité')
plt.ylabel('Prénom')
plt.show()