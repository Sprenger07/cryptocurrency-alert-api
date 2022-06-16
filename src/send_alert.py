import requests

import json
from pydantic import BaseModel
import pymongo
from pymongo import MongoClient

import constants
from methods import *

url = 'https://rest.coinapi.io/v1/assets'
headers = COIN_API_KEY
response = requests.get(url, headers=headers)


if response.status_code == 429:
    raise "To many request to Coin API"


# To a list of all alert to send
#GET /alert/

def get_all_alert_to_send():
    list_of_all_alert = []
    jsonResponse = response.json()

    for i in range(LIMITER):
        data = jsonResponse[i]

        if limiteur >= 1000:
            break

        try:
            price = int(data["price_usd"])
            currency = str(data["asset_id"])
            query = {"$and" : 
                    [{"currency" : currency }, 
                    {"$or" : 
                        [{"$and" : 
                            [{"price": { "$gte": price }}, 
                            {"method" : "below"}]
                        }, 
                        {"$and" : 
                            [{"price": { "$lte": price }},
                             {"method" : "above"}]
                        }]
                    }]
                }
            list_of_all_alert += alertsEntity(alert_db.find(query))
        except:
            continue
    return list_of_all_alert


# To a list of all alert to send

def sends_Message(list_of_alert):
    for data in list_of_alert:
        mail = data["mail"]

        currency = data["currency"]
        method = data["method"]
        price = data["price"]

        content = f"Message for {mail} : The price of {currency} is {method} ${price}"
        print(content)


if __name__ == "__main__":
    sends_Message(get_all_alert_to_send())
