import json
import pymongo

#just some file to check some stuff.
json_str = '{"username": "worldxdana", "password": "123qwe123"}'
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["users"]
