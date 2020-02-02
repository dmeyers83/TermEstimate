from pymongo import MongoClient
#https://api.mongodb.com/python/current/tutorial.html
from datetime import datetime

class dbConnection:
    client = MongoClient()
    testhost = "localhost"
    testIP = 3001
    devURI = "mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb"
    prodURI = ""
    nameDB = ""
    nameCollection = ""

    def __init__(self, devEnv = True, DB = 'termestimate', collection='job_keywords'):

        if devEnv == True:
            self.client = MongoClient(self.devURI)
        else:
            self.client = MongoClient(self.prodURI)
            DB = 'askbezos'

        self.nameDB = self.client[DB]

        self.nameCollection = self.nameDB[collection]

    def insertData(self, jsonObject):
        self.nameCollection.insert_many(jsonObject)

    def returnUniqueQueryValues(self):
        return self.nameCollection.distinct("query")

    def returnQueryValues(self, query):
        result = self.nameCollection.find({"query":query, "keyword_count" : {"$gte" : 10}},{"_id": 0, "time":0 })
        list_result = list(result)
        print (list_result)
        return (list_result)