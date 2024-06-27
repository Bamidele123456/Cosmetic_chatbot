from pymongo import MongoClient, UpdateOne, DeleteMany
from pymongo.server_api import ServerApi

# MongoDB connection
uri = "mongodb+srv://Bamidele:1631324de@cluster0.hrdikjw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['Data']
hello = db['test']
hello.insert_one({"hello":"why"})


try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
