from pymongo import MongoClient

def get_database():
   CONNECTION_STRING = "mongodb://root:random@localhost"
   client = MongoClient(CONNECTION_STRING)
   return client["animalclassifier"]