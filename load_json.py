import json
import sys
from pymongo import MongoClient 
'''
def main():
    # obtain DB port number
    if len(sys.argv) != 2:
        print("No port given")
        exit(0)
    portNo = sys.argv[1]
    dbName = "291db"
    
    # setup connection to MongoDB
    client, db = connectPort(portNo, dbName)
    # get collections 
    collection = db.list_collection_names()   
    
    client, db, = loadData(client, db, collection)
'''
def connectPort(portNo, dbName):
    # initialize connection to MongoDB. Return db and client
    portNo = portNo.strip()
    portNo = int(portNo)

    dbpath = 'mongodb://localhost:{}'.format(portNo)
    client = MongoClient(dbpath)
    db = client[dbName]

    return client, db

def loadData(client, db, collection):
    # create collections and checks 
    name_basics = db['name_basics']
    title_basics = db['title_basics']
    title_principals = db['title_principals']
    title_ratings = db['title_ratings']

    # drop existing collections
    if not set(['name_basics', 'title_basics', 'title_principals', 'title_ratings']).isdisjoint(collection):
        name_basics.drop()
        title_basics.drop()
        title_principals.drop()
        title_ratings.drop()
        print("Dropped")
    else:
        print("No duplicate collections found.")

    print("Creating collections...")
     
    # open json and load to collection
    with open('name.basics.json', encoding="utf8") as f:
        data1 = json.load(f)
    name_basics.insert_many(data1)
    f.close()

    with open('title.basics.json', encoding="utf8") as f:
        data2 = json.load(f)
    title_basics.insert_many(data2)
    f.close()

    with open('title.principals.json', encoding="utf8") as f:
        data3 = json.load(f)
    title_principals.insert_many(data3)
    f.close()

    with open('title.ratings.json', encoding="utf8") as f:
        data4 = json.load(f)
    title_ratings.insert_many(data4)
    f.close()

    print("Collections created")

    return client, db

#main()
