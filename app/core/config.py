import os

# Mongo DB Settings
MONGODB_URL = os.getenv("MONGODB_URL", "NOT_A_REAL_MONGODB")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_USER = os.getenv("MONGO_USER", "admin")
MONGO_PASS = os.getenv("MONGO_PASSWORD", "fill_me_in")
MONGO_DB = os.getenv("MONGO_DB", "fastapi")
if not MONGODB_URL:
    MONGODB_URL = f'mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}'

database_name = 'portfolio_mgmt'
pnl_collection_name = 'realized_pnl'
raw_positions_collection_name = 'positions'
trade_collection_name = 'trades'
