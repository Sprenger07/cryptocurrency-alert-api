import pymongo
from pymongo import MongoClient
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import List
import json

from constants import *
from methods import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    cluster.server_info()

except:
    raise "Error you are Not connected to the DataBase"



@app.get("/")
async def home():
    return {"hello" : "word"}


# To get all alert
#GET /alert/

@app.get("/alert/", response_model=List[Alert])
async def get_my_alert(mail : str):
    try:
        return alertsEntity(alert_db.find({"mail" : mail}))
    except:
        raise HTTPException(status_code=404, detail="ERROR")

# To post an alert
#POST /alert/

@app.post("/alert/" , response_model=Alert)
async def  create_alert(mail : str, currency : str, price: int, method : str):
    try :
        alert = {"mail" : mail, "currency" : currency, "price" : price, "method" : method}
        alert_db.insert_one(alert)
        return alert
    except:
        raise HTTPException(status_code=404, detail="ERROR")


# To delete particular alert
#DELETE /alert/

@app.delete("/alert/", response_model=Alert)
async def delete_alert(mail : str, currency : str, price: int, method : str):
    try:
        alert = {"mail" : mail, "currency" : currency, "price" : price, "method" : method}
        if alert_db.find(alert)[0]:
            alert_db.delete_one(alert)
            return alert
    except:
        raise HTTPException(status_code=404, detail="Alert do not exist")

