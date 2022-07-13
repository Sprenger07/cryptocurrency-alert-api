import pymongo
from pymongo import MongoClient
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import List
import json
import hashlib

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


# To post user
# POST /user/

@app.post("/user/", response_model=User, response_model_exclude={"password"})
async def create_user(mail, password):
    try:
        if not usersEntity(userlist_db.find({"mail": mail})):
            password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            new_user = {"mail": mail, "password": password}
            userlist_db.insert_one(new_user)
            return {"mail": mail, "password": password}
        else:
            raise
    except:
        raise HTTPException(status_code=404, detail="User already exist")


# To get all users
# GET /all_users/

@app.get("/all_user/", response_model=List[User], response_model_exclude={"password"})
async def get_user():
    try:
        return usersEntity(userlist_db.find({}))
    except:
        raise HTTPException(status_code=404, detail="Impossible to load the database")


# To get one user
# GET /user/

@app.get("/user/", response_model=User, response_model_exclude={"password"})
async def get_user(mail: str, password: str):
    try:
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if usersEntity(userlist_db.find({"mail": mail, "password": password})):
            return {"mail": mail, "password": password}
        raise
    except:
        if usersEntity(userlist_db.find({"mail": mail})):
            raise HTTPException(status_code=404, detail="Wrong Password")
        else:
            raise HTTPException(status_code=404, detail="User do not exist")


# To update particular user
# PUT /user/

@app.put("/user/", response_model=User, response_model_exclude={"password"})
async def update_password(mail, old_password, new_password):
    try:
        password = hashlib.sha256(old_password.encode('utf-8')).hexdigest()
        if usersEntity(userlist_db.find({"mail": mail, "password": password}))[0]:
            password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
            userlist_db.update_one({"mail": mail}, {"$set": {"password": password}})
            return {"mail": mail, "password": password}
        raise
    except:
        raise HTTPException(status_code=404, detail="Wrong mail or password")


# To delete particular user
# DELETE /user/

@app.delete("/user/", response_model=User, response_model_exclude={"password"})
async def delete_user(mail, password):
    try:
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if usersEntity(userlist_db.find({"mail": mail, "password": password})):
            userlist_db.delete_one({"mail": mail, "password": password})
            return ({"mail": mail, "password": password})
    except:
        raise
    else:
        raise HTTPException(status_code=404, detail="Wrong User or password")


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
        if method == "above" or method == "below":
            alert = {"mail" : mail, "currency" : currency, "price" : price, "method" : method}
            alert_db.insert_one(alert)
            return alert
        raise
    except:
        error_message = "Error"
        if not (method == "above" or method == "below"):
            error_message = "Wrong syntax method, method should be 'below' or 'above'"
        raise HTTPException(status_code=404, detail=error_message)
        

# To delete particular alert
#DELETE /alert/

@app.delete("/alert/", response_model=Alert)
async def delete_alert(mail : str, currency : str, price: int, method : str):
    try:
        alert = {"mail" : mail, "currency" : currency, "price" : price, "method" : method}
        if alert_db.find(alert)[0]:
            alert_db.delete_one(alert)
            return alert
        else:
            raise
    except:
        raise HTTPException(status_code=404, detail="Alert do not exist")


@app.delete("/all_alert/", response_model=List[Alert])
async def delete_all_alert(mail : str):
    try:
        all_alert = alertsEntity(alert_db.find({"mail": mail}))
        if all_alert:
            alert_db.delete_many({"mail": mail})
            return all_alert
        else:
            raise
    except:
        raise HTTPException(status_code=404, detail="You dont have alert")