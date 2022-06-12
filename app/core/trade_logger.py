from app.db.mongo_db_service import MongoDBService

def log_trade(trade):
    mongo_server = MongoDBService()
    db = mongo_server['positions_db']
