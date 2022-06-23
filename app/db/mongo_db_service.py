import logging
from app.core.config import MONGODB_URL, database_name
from pymongo import MongoClient


class MongoDBService():
    def __init__(self):
        self.url = MONGODB_URL
        self.db_name = database_name
        self.client = None

    def connect_client(self):
        logging.info("Creating connection to MongoDB instance...")
        self.client = MongoClient(self.url)
        self.db = self.client[self.db_name]
        logging.info("Successfully created connection.")

    def close_client(self):
        logging.info("Closing connection to MongoDB instance...")
        self.client.close()
        logging.info("Successfully closed connection.")

    def query(self, collection_name, query):
        mongo_collection = self.db[collection_name]
        return list(mongo_collection.find(query))

    def query_most_recent(self, collection_name, query, time_field='update_time'):
        mongo_collection = self.db[collection_name]
        return mongo_collection.find_one(query, sort=[(time_field, -1)])

    def insert(self, collection_name, data):
        mongo_collection = self.db[collection_name]
        status = mongo_collection.insert_one(data)
        return status

    def delete(self, collection_name, query):
        mongo_collection = self.db[collection_name]
        status = mongo_collection.delete_many(query)
        return status

    def update(self, collection_name, query, update_fields):
        mongo_collection = self.db[collection_name]
        mongo_collection.update_many(query, update_fields)

