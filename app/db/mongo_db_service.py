from app.core.config import MONGODB_URL
import pymongo

class MongoDBService():
    def __init__(self):
        self.url = MONGODB_URL
        self.client = pymongo.MongoClient(self.url)