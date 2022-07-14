from pymongo import MongoClient

from dotenv import load_dotenv

import os

load_dotenv()

MONGO_DB = os.getenv("MONGO_DB_SERV")
API_KEY = os.getenv("KEY")


# Please put your own database

# cluster = MongoClient("mongodb://Login:Password@localhost:27017")
cluster = MongoClient(MONGO_DB)

db = cluster["Seelk"]
alert_db = db["alert"]
userlist_db = db["userlist"]



# Get your own key at the following address: https://www.coinapi.io/
COIN_API_KEY = {"X-CoinAPI-Key": f"{API_KEY}"}

