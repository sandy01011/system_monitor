import gridfs
import pymongo
import json
from monmeta import meta


metadata= meta()
db = metadata[3]
db_collection = metadata[4]

class MongoDB(object):
    metadata = meta()
    username = metadata[0]
    password = metadata[1]
    URI = metadata[2]
    db = metadata[3]
    db_collection = metadata[4]
    DATABASE = None


    @staticmethod
    def initialize(db):
        try:
            client = pymongo.MongoClient(MongoDB.URI)
            MongoDB.DATABASE = client[MongoDB.db]
            MongoDB.DATABASE.authenticate(MongoDB.username, MongoDB.password)
        except Exception:
            print("Fatal error in main loop")

    @staticmethod
    def insert(collection, data):
        MongoDB.DATABASE[collection].insert(data, check_keys=False)

    @staticmethod
    def insertmany(collection, data):
        MongoDB.DATABASE[collection].insert(data)


def load_monitor_data(mondb,data):
    MongoDB.initialize(db)
    #print('mongodb initialized')
    #print('current db is {} collection is {} while data is {}'.format(db, db_collection, data))
    try:
        MongoDB.insert(collection=db_collection,data=data)
    except Exception:
        print('load_bot_meta_to_db error occured')


#class LoadData(object):
#    meta = meta()
#    db = meta[3]
#    MongoDB.initialize(db)
#    
#    def load_monitor_data(data):
#         #print('type of df is{} and value of df is {}'.format(type(self.df), self.df))
#         print(type(data))
#         try:
#             print('h')
#             MongoDB.insert(collection=data['prime']['node_name'],data=data)
#         except Exception:
#             print('load_bot_meta_to_db error occured')
#
