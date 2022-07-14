from methods import *

url = 'https://rest.coinapi.io/v1/assets'
headers = COIN_API_KEY
response = requests.get(url, headers=headers)

if response.status_code == 429:
    raise "To many request to Coin API"

try:
    cluster.server_info()

except:
    raise "Error you are Not connected to the DataBase"


def db_filter(currency, price):
    query = {"$and":
                 [{"currency": currency},
                  {"$or":
                       [{"$and":
                             [{"price": {"$gte": price}},
                              {"method": "below"}]
                         },
                        {"$and":
                             [{"price": {"$lte": price}},
                              {"method": "above"}]
                         }]
                   }]
             }
    return query


# To a list of all alert to send
# GET /alert/

def get_all_alert_to_send():
    list_cryto = alert_db.distinct('currency')
    list_of_all_alert = []
    for curr in list_cryto:
        url_curr = f'https://rest.coinapi.io/v1/assets/{curr}'
        response_curr = (requests.get(url_curr, headers=headers))
        data = response_curr.json()

        price = data[0]["price_usd"]

        query = db_filter(curr, price)
        list_of_all_alert += alerts_entity(alert_db.find(query))
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
