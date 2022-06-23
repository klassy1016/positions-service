import os

# Mongo DB Settings
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb+srv://positions_ro:4Gof3geGquEWLMw2@cluster0.lxlgw.mongodb.net/?retryWrites=true&w=majority")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_USER = os.getenv("MONGO_USER", "admin")
MONGO_PASS = os.getenv("MONGO_PASSWORD", "fill_me_in")
MONGO_DB = os.getenv("MONGO_DB", "fastapi")
if not MONGODB_URL:
    MONGODB_URL = f'mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}'
MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))

database_name = 'portfolio_mgmt'

pnl_collection_name = 'realized_pnl'
raw_positions_collection_name = "positions"
trade_collection_name = "trades"