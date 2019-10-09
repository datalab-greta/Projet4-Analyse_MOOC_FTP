import pprint, os, pandas

from sqlalchemy import create_engine
from sqlalchemy.sql import text

from pymongo import MongoClient # librairie qui va bien
import configparser

config = configparser.ConfigParser()
config.read_file(open(os.path.expanduser("~/.datalab.cnf")))

CNF = "mongo"
BDD = "Datalab"
# Ouverture connection -> mongo sur serveur
client = MongoClient('mongodb://%s:%s@%s/?authSource=%s' % (config[CNF]['user'], config[CNF]['password'], config[CNF]['host'], BDD))
print(client)

TBL = "Forum_1"
CNF2 = "pgBDD"
pgSQLengine = create_engine("postgresql://%s:%s@%s/%s" % (config[CNF2]['user'], config[CNF2]['password'], config[CNF2]['host'], "BDD_PASCALE"))
print(pgSQLengine)
pgSQLengine.execute("""CREATE TABLE 'Forum_1'(
   id VARCHAR (50) UNIQUE NOT NULL,
   course_id VARCHAR (50) UNIQUE NOT NULL,
   date VARCHAR (50) NOT NULL,
   username VARCHAR (355) UNIQUE NOT NULL
);""")
#pgSQLengine.execute("TRUNCATE \"%s\";" % TBL)

statement = text("""
INSERT INTO "Forum" (id, course_id, date, username)
VALUES (:id, :cid, :date, :username)""")
#~ exit()

bdd = client['Datalab'] # BDD "Datalab" de mongoDB sur serveur
bdd
#~ print("'Datalab' Collections:")
#~ for cn in bdd.list_collection_names():
    #~ print("-"+cn)
collec = client['Datalab']['MoocZip_Tarik']

def applat(mesg, niv):
    l = len(mesg['body'])
    print("%s %s %s : %s = %d" % ("  "*niv, mesg['course_id'], mesg['updated_at'], mesg['username'], l))
    pgSQLengine.execute(statement, id=mesg['id'], cid=mesg['course_id'], date=mesg['updated_at'], username=mesg['username'])
    childs = [] # liste des enfants
    if 'children' in mesg: childs += mesg['children']
    if 'endorsed_responses' in mesg: childs += mesg['endorsed_responses']
    if 'non_endorsed_responses' in mesg: childs += mesg['non_endorsed_responses']
    for child in childs:
        applat(child, niv+1)
    
'''    if 'children' in mesg:
        for child in mesg['children']:
            #~ print("CCC")
            applat(child, niv+1)
    if 'endorsed_responses' in mesg:
        for child in mesg['endorsed_responses']:
            #~ print("EEE")
            applat(child, niv+1)
    if 'non_endorsed_responses' in mesg:
        for child in mesg['non_endorsed_responses']:
            #~ print("NNN")
            applat(child, niv+1)
'''

cursor = collec.find()
for doc in cursor:
    if 'content' in doc:
        #~ pprint.pprint(doc)
        print("-------------------------------")
        applat(doc['content'], 0)
