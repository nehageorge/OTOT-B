import pymongo

client = pymongo.MongoClient('mongodb://mongodb:27017', connect=False)
db = client.NUS
col = db["ImageRepo"]

col.delete_many({})
