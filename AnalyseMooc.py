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
#graph lib
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords 
#Librairie pour compter
import collections
#list_file= os.listdir('/home/tarik/Documents/Projet4_machine learning/Documents_json/course-v1_CNAM+01032+session01')
#path= '/home/tarik/Documents/Projet4_machine learning/Documents_json/course-v1_CNAM+01032+session01'


list_id=[]
list_username=[]
list_threadtype=[]
list_courseware_title=[]
list_body=[]
#dict_username={}
rootdir = '/home/tarik/Documents/Projet4_machine learning/Documents_json/'

for subdir, dirs, list_file in os.walk(rootdir):


    for file in list_file:
        #print (os.path.join(subdir, file))
    
# Definition du chemin de fichier
        with open(os.path.join(subdir, file),'r',encoding="utf8") as f:
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
                body= python_dict['content']['body']
                #print(username)
                list_id.append(_id)
                list_username.append(username)
                list_courseware_title.append(courseware_title)
                list_threadtype.append(thread_type)
                list_body.append(body)
                #dict_username[file] = username
            except KeyError:
                pass
                
                #list_username.append('undefined')
                #list_courseware_title.append('undefined')
                #list_threadtype.append('undefined')
                #dict_username[file] = 'undefined'        

#pd.set_option("display.colheader_justify","right")
df = pd.DataFrame({"id":list_id,"username":list_username,"nom_du_cours":list_courseware_title,
                   "thread_type":list_threadtype,"body":list_body})

print(df)
#Librairie pour compter
import collections
#comptage_tout = collections.Counter(list_username)# Compte TOUT 
#comptage_top = collections.Counter(list_username).most_common(20)# Compte les 20 premiers
#print(comptage_tout)
#print('###########################')
#print(comptage_top)

# HISTROGRAMME DES 20 USERNAME LES PLUS UTILISE

#fig = plt.figure(1, figsize=(30, 20))
#plt.bar(*zip(*comptage_top))
#plt.title('Top 20 des username')
#plt.xlabel('Quantité')
#plt.ylabel('Prénom')
#plt.show()

#data frame avec users par cours
tab_courses =(pd.crosstab(df['username'],df['nom_du_cours'],
                  rownames=['usernames'],
                  colnames=['coursenames']))
tab_courses

comptage_users= collections.Counter(list_username)# Compte les users

#data frame avec users par coursthread_type
tab_discussion_users =(pd.crosstab(df['username'],df['thread_type']).sort_values('discussion',ascending=False))
#print(tab_discussion_users)

#graph stackbar thread_type
#tab_discussion[:20].plot(kind='bar', stacked =True, color=['blue','yellow'])#empile
tab_discussion_users[:20].plot(kind='barh', stacked =True,color=['blue','yellow'])#empile à l'horizontal 'barh'

#Graphique popularité des cours
plt.figure(figsize=(30, 20))
sns.set(style="darkgrid")
plt.xticks(rotation=90)
ax = sns.countplot(y="nom_du_cours", data=df)

#data frame avec courses par coursthread_type
tab_discussion_courses =(pd.crosstab(df['nom_du_cours'],df['thread_type']).sort_values('discussion',ascending=False))
#print(tab_discussion)

#graph stackbar thread_type
tab_discussion_courses[:20].plot(kind='barh', stacked =True,color=['DarkBlue','LightGreen'])#empile à l'horizontal 'barh'

#World Cloud

# Start with one review:

stopwrd= stopwords.words('french')
stopwrd.extend(STOPWORDS)
stopwrd.extend(['d\'un'])
print(stopwrd)
# Create and generate a word cloud image from username:

text = df.body.values
wordcloud = WordCloud(
    width = 3000,
    height = 2000,
    background_color = 'white',
    stopwords = stopwrd).generate(str(text))
fig = plt.figure(
    figsize = (40, 30),
    facecolor = 'k',
    edgecolor = 'k')
plt.imshow(wordcloud, interpolation = 'bilinear')
plt.axis('off')
plt.tight_layout(pad=0)
plt.show()

