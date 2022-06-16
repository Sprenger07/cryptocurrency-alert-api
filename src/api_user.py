import hashlib

import pymongo
from pymongo import MongoClient
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Optional, List
from pydantic import BaseModel

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

@app.get("/")
async def home():
    return {"hello" : "world"}


# To post user
#POST /user/

@app.post("/user/", response_model=User, response_model_exclude={"password"})
async def create_user(mail, password):
    try: 
        if not usersEntity(userlist_db.find({"mail" : mail})):
            password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            new_user = {"mail" : mail, "password" : password}
            userlist_db.insert_one(new_user)
            return new_user
    except:
        raise HTTPException(status_code=404, detail="User already exist")


# To get all users
#GET /all_users/

@app.get("/all_user/", response_model=List[User], response_model_exclude={"password"})
async def get_user():
    try:
        return usersEntity(userlist_db.find({}))
    except:
        raise HTTPException(status_code=404, detail="User already exist")



# To get one user
#GET /user/

@app.get("/user/", response_model=User, response_model_exclude={"password"})
async def get_user(mail : str):
    try:
        return usersEntity(userlist_db.find({"mail" : mail}))[0]
    except:
        raise HTTPException(status_code=404, detail="User do not exist")


# To update particular user
#PUT /user/

@app.put("/user/", response_model=User, response_model_exclude={"password"})
async def update_password(mail, old_password, new_password):

    try:
        password = hashlib.sha256(old_password.encode('utf-8')).hexdigest()
        if usersEntity(userlist_db.find({"mail" : mail, "password" : password})):
            password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
            userlist_db.update_one({"mail" : mail}, {"$set":{"password" : password}})
            return {"mail" : mail, "password" : password}
    except:
        raise HTTPException(status_code=404, detail="Wrong mail or password")

# To delete particular user
#DELETE /user/

@app.delete("/user/", response_model=User, response_model_exclude={"password"})
async def delete_user(mail, password):
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    if usersEntity(userlist_db.find({"mail" : mail, "password" : password})):
        userlist_db.delete_one({"mail" : mail, "password" : password})
        return ({"mail" : mail, "password" : password})
    else:
        raise HTTPException(status_code=404, detail="Wrong User or password")

    




