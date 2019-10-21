import pprint, os, pandas

from sqlalchemy import create_engine
from sqlalchemy.sql import text

from pymongo import MongoClient # librairie qui va bien
import configparser

config = configparser.ConfigParser()
config.read_file(open(os.path.expanduser("~/.datalab.cnf")))

CNF = "mongoBDD"
BDD = "Datalab"
# Ouverture connection -> mongo sur serveur
client = MongoClient('mongodb://%s:%s@%s/?authSource=%s' % (config[CNF]['user'], config[CNF]['password'], config[CNF]['host'], BDD))
print(client)

TBL = "MoocZip"
CNF = "pgBDD"
pgSQLengine = create_engine("postgresql://%s:%s@%s/%s" % (config[CNF]['user'], config[CNF]['password'], config[CNF]['host'], "BDD_Tarik"))
print(pgSQLengine)

pgSQLengine.execute("""CREATE TABLE IF NOT EXISTS "MoocZip"(
   id VARCHAR (50)  NOT NULL,
   course_id VARCHAR (50)  NOT NULL,
   date DATE NOT NULL,
   username VARCHAR (355)  NOT NULL,
   level SMALLINT  NOT NULL,
   message VARCHAR (6000)  NOT NULL
);""")
#pgSQLengine.execute("TRUNCATE \"%s\";" % TBL)#pgSQLengine.execute("TRUNCATE \"%s\";" % TBL)
statement = text("""
INSERT INTO "MoocZip" (id, course_id, date, username, level, message)
VALUES (:id, :cid, :date, :username, :level, :message)""")
#~ exit()

bdd = client['Datalab'] # BDD "Datalab" de mongoDB sur serveur
bdd
#~ print("'Datalab' Collections:")
#~ for cn in bdd.list_collection_names():
    #~ print("-"+cn)
collec = client['MOOC_GRP_FTP']['MoocZip_Tarik']

       


NivMax = 0

def applat(mesg, niv):
    global NivMax
    l = len(mesg['body'])
    username = '?'
    
    if 'username' in mesg: username = mesg['username'][:50]
    #c = len(mesg['endorsed_responses']+mesg['non_endorsed_responses'])

    pgSQLengine.execute(statement, id=mesg['id'], cid=mesg['course_id'], date=mesg['updated_at'], username=username, level=niv, message=mesg['body'])
    childs = [] # liste des enfants
    if 'children' in mesg: childs += mesg['children']
    if 'endorsed_responses' in mesg: childs += mesg['endorsed_responses']
    if 'non_endorsed_responses' in mesg: childs += mesg['non_endorsed_responses']
    for child in childs:
#        applat(child+l, niv+1)
        l+=applat(child,niv+1)
    #print("nombre de caractères cumulés ",l)
    if niv > NivMax:
        NivMax = niv
    print("%s %s %s : %s = %d,%d" % ("  "*niv, mesg['course_id'], mesg['updated_at'], username,len(mesg['body']),l))
    return l

cursor = collec.find()
for doc in cursor:
    if 'content' in doc:
        #~ pprint.pprint(doc)
        print("-------------------------------")
        longueur = applat(doc['content'], 0)
        #~ print(longueur)
        
print("Niv max=%d" % NivMax)
