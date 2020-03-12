from pymongo import MongoClient
#https://api.mongodb.com/python/current/tutorial.html
from datetime import datetime
import json
import pandas as pd

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
        self.nameDB = self.client[DB]

        self.nameCollection = self.nameDB[collection]

    def insertData(self, jsonObject):
        self.nameCollection.insert_many(jsonObject)

    def returnUniqueQueryValues(self):
        return self.nameCollection.distinct("query")

    def returnKeywordValues(self, query,limit_amount=75):
        return_amount =3

        result = self.nameCollection.find({"query":query, "keyword_count" : {"$gte" : 2}},{"_id": 0, "time":0 }).sort("keyword_count", -1).limit(limit_amount)
        list_result = list(result)
        nouns = [x for x in list_result if x['POS'] == 'Noun'][: return_amount]
        print("nouns")
        print(nouns)
        verbs = [x for x in list_result if x['POS'] == 'Verb'][: return_amount]
        print("verbs")
        print(verbs)
        adjectives = [x for x in list_result if x['POS'] == 'Adjective'][: return_amount]
        print("adjectives")
        print(adjectives)
        adverbs = [x for x in list_result if x['POS'] == 'Adverb'][: return_amount]
        print (list_result)
        topNum = list_result[0]['keyword_count']
        print("Top keyword count")
        print(topNum)
        return ({"all":list_result,"nouns":nouns,"verbs":verbs,"adjectives":adjectives, "adverbs":adverbs,"high_keyword":topNum})

    def returnQueryValues(self, keyword, limit_amount=5):
        result = self.nameCollection.find({"keyword": keyword}, {"_id": 0, "time": 0}).sort("keyword_count", -1).limit(limit_amount)
        list_result = list(result)


        print (list_result)
        return (list_result)

    def insert_df(self, df):
        records = json.loads(df.T.to_json()).values()
        self.nameCollection.insert_many(records)