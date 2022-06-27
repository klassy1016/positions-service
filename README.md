# positions-service

A simple HTTP service that supports basic functionality required
for trading and managing financial instruments.

### Features
- Trade logging
- Active position tracking
- Realized pnl tracking
- Grouping trades, positions, and pnl by trader, portfolio, strategy & asset class

### Tech
The service is written in Python using the [FastAPI](https://github.com/tiangolo/fastapi) framework. [MongoDB](https://www.mongodb.com) is used as the persistent
data store.

### Installation
1. Clone and create the virtual environment.
```sh
git clone "https://github.com/klassy1016/positions-service.git"
cd positions-service
conda env create -f environment.yml
conda activate positions-service
```
2. Create a free MongoDB database [here](https://www.mongodb.com/basics/create-database).
3. Set the MONGODB_URL environment variable to your created database's connection string.
```sh
export MONGODB_URL=<your_db_connection_string>
```
4. Run the service locally
```sh
uvicorn --host 0.0.0.0 --port 8000 app.main:app --workers 4
```

At this point, your service should now be running.
You can visit the /docs endpoint to find more information on the supported endpoints.

### Dependencies
 - Python 3.8+
 - Uvicorn
 - Anaconda
 - MongoDB (database set up)
