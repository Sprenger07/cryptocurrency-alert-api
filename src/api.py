from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from typing import List
import hashlib

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
    return {"hello": "word"}


# To post user
# POST /user/


@app.post("/user/", response_model=User, response_model_exclude={"password"})
async def create_user(mail: str, password: str):
    try:
        if not is_valid_mail(mail):
            raise MailError
        if not is_valid_password(password):
            raise PasswordError

        if not users_entity(userlist_db.find({"mail": mail})):
            password = hashlib.sha256(password.encode("utf-8")).hexdigest()
            new_user = {"mail": mail, "password": password}
            userlist_db.insert_one(new_user)
            return {"mail": mail, "password": password}
        else:
            raise UserExistError
    except MailError:
        raise HTTPException(status_code=404, detail="Invalid mail")
    except PasswordError:
        raise HTTPException(
            status_code=404,
            detail="Your password must contain eight characters, at least one "
            "letter, one number and one special character",
        )
    except UserExistError:
        raise HTTPException(status_code=404, detail="User already exist")
    except:
        raise HTTPException(status_code=404, detail="Error")


# To get one user
# GET /user/


@app.get("/user/", response_model=User, response_model_exclude={"password"})
async def get_user(mail: str, password: str):
    try:
        password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        if users_entity(userlist_db.find({"mail": mail, "password": password})):
            return {"mail": mail, "password": password}
        raise
    except:
        if users_entity(userlist_db.find({"mail": mail})):
            raise HTTPException(status_code=404, detail="Wrong Password")
        else:
            raise HTTPException(status_code=404, detail="User do not exist")


# To update particular user
# PUT /user/


@app.put("/user/", response_model=User, response_model_exclude={"password"})
async def update_password(mail: str, old_password: str, new_password: str):
    try:
        if not is_valid_password(new_password):
            raise PasswordError

        password = hashlib.sha256(old_password.encode("utf-8")).hexdigest()
        if users_entity(userlist_db.find({"mail": mail, "password": password}))[0]:
            password = hashlib.sha256(new_password.encode("utf-8")).hexdigest()
            userlist_db.update_one({"mail": mail}, {"$set": {"password": password}})
            return {"mail": mail, "password": password}
        raise
    except PasswordError:
        raise HTTPException(
            status_code=404,
            detail="Your password must contain eight characters, at least one "
            "letter, one number and one special character",
        )
    except:
        raise HTTPException(status_code=404, detail="Wrong mail or password")


# To delete particular user and his alert in the same time
# DELETE /user/


@app.delete("/user/", response_model=User, response_model_exclude={"password"})
async def delete_user(mail: str, password: str):
    try:
        password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        if users_entity(userlist_db.find({"mail": mail, "password": password})):
            userlist_db.delete_one({"mail": mail, "password": password})

            all_alert = alerts_entity(alert_db.find({"mail": mail}))
            if all_alert:
                alert_db.delete_many({"mail": mail})

            return {"mail": mail, "password": password}
    except:
        raise
    else:
        raise HTTPException(status_code=404, detail="Wrong User or password")


# To get all alert
# GET /alert/


@app.get("/alert/", response_model=List[Alert])
async def get_my_alert(mail: str, password: str):
    try:
        return alerts_entity(alert_db.find({"mail": mail}))
    except:
        raise HTTPException(status_code=404, detail="ERROR")


# To post an alert
# POST /alert/


@app.post("/alert/", response_model=Alert)
async def create_alert(
    mail: str, password: str, currency: str, price: int, method: str
):
    try:
        if not (method == "above" or method == "below"):
            raise MethodError

        if not is_valid_currency(currency):
            raise CurrencyError

        password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        if not users_entity(userlist_db.find({"mail": mail, "password": password})):
            raise UserNotFoundError

        alert = {"mail": mail, "currency": currency, "price": price, "method": method}
        alert_db.insert_one(alert)
        return alert

    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found in database")

    except MethodError:
        raise HTTPException(
            status_code=404,
            detail="Wrong syntax method, method should be 'below' or 'above'",
        )

    except CurrencyError:
        raise HTTPException(
            status_code=404, detail="Crypto currency is not available on COINS-API"
        )

    except CoinApiError:
        url = "https://rest.coinapi.io/v1/assets"
        headers = COIN_API_KEY
        response = requests.get(url, headers=headers)

        raise HTTPException(
            status_code=404,
            detail=f"There is a problem with COINS-API, code error :{response.status_code}",
        )

    except:
        raise HTTPException(status_code=404, detail="error")


# To delete particular alert
# DELETE /alert/


@app.delete("/alert/", response_model=Alert)
async def delete_alert(
    mail: str, password: str, currency: str, price: int, method: str
):
    try:
        alert = {"mail": mail, "currency": currency, "price": price, "method": method}
        if alert_db.find(alert)[0]:
            alert_db.delete_one(alert)
            return alert
        else:
            raise AlertError
    except AlertError:
        raise HTTPException(status_code=404, detail="Alert do not exist")
    except:
        raise HTTPException(status_code=404, detail="error")
