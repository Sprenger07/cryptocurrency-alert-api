import pymongo
from pymongo import MongoClient

# Please put your own database
cluster = MongoClient("mongodb://mongoAdmin:changeMe@37.187.55.169:27017")
db = cluster["Seelk"]
alert_db = db["alert"]
userlist_db = db["userlist"]

# Get your own key at the following address: https://www.coinapi.io/
COIN_API_KEY = {'X-CoinAPI-Key' : 'CD4B6E6E-BBE4-4D87-8142-FED6064FD80F'}


# Variable to limit the execution time of the program but you are free to modify this value at your convenience 
LIMITER = 1000