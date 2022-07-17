from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from typing import List
import hashlib

import methods
import constants

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    constants.cluster.server_info()
except Exception:
    raise "Error you are Not connected to the DataBase"


@app.get("/")
async def home():
    return {"hello": "word"}


# To post user
# POST /user/


@app.post("/user/", response_model=methods.User,
          response_model_exclude={"password"})
async def create_user(mail: str, password: str):
    try:
        if not methods.is_valid_mail(mail):
            raise methods.MailError
        if not methods.is_valid_password(password):
            raise methods.PasswordError

        query = {"mail": mail}
        if not methods.users_entity(constants.userlist_db.find(query)):
            password = hashlib.sha256(password.encode("utf-8")).hexdigest()
            new_user = {"mail": mail, "password": password}
            constants.userlist_db.insert_one(new_user)
            return {"mail": mail, "password": password}
        else:
            raise methods.UserExistError
    except methods.MailError:
        raise HTTPException(status_code=404, detail="Invalid mail")
    except methods.PasswordError:
        raise HTTPException(
            status_code=404,
            detail="Your password must contain eight characters, at least one "
                   "letter, one number and one special character",
        )
    except methods.UserExistError:
        raise HTTPException(status_code=404, detail="User already exist")
    except Exception:
        raise HTTPException(status_code=404, detail="Error")


# To get one user
# GET /user/


@app.get("/user/", response_model=methods.User,
         response_model_exclude={"password"})
async def get_user(mail: str, password: str):
    try:
        password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        query = {"mail": mail, "password": password}
        if methods.users_entity(constants.userlist_db.find(query)):
            return {"mail": mail, "password": password}
        raise methods.UserNotFoundError

    except methods.UserNotFoundError:
        if methods.users_entity(constants.userlist_db.find({"mail": mail})):
            raise HTTPException(status_code=404, detail="Wrong Password")
        else:
            raise HTTPException(status_code=404, detail="User do not exist")
    except Exception:
        raise HTTPException(status_code=404, detail="Error")


# To update particular user
# PUT /user/


@app.put("/user/", response_model=methods.User,
         response_model_exclude={"password"})
async def update_password(mail: str, old_password: str, new_password: str):
    try:
        if not methods.is_valid_password(new_password):
            raise methods.PasswordError

        password = hashlib.sha256(old_password.encode("utf-8")).hexdigest()
        if methods.users_entity(constants.userlist_db.find(
                {"mail": mail, "password": password}))[0]:
            password = hashlib.sha256(new_password.encode("utf-8")).hexdigest()
            constants.userlist_db.update_one(
                {"mail": mail}, {"$set": {"password": password}})
            return {"mail": mail, "password": password}
        raise
    except methods.PasswordError:
        raise HTTPException(
            status_code=404,
            detail="Your password must contain eight characters, at least one "
            "letter, one number and one special character",
        )
    except Exception:
        raise HTTPException(status_code=404, detail="Wrong mail or password")


# To delete particular user and his alert in the same time
# DELETE /user/


@app.delete("/user/", response_model=methods.User,
            response_model_exclude={"password"})
async def delete_user(mail: str, password: str):
    try:
        password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        query = {"mail": mail, "password": password}
        if methods.users_entity(constants.userlist_db.find(query)):
            constants.userlist_db.delete_one(query)

            all_alert = methods.alerts_entity(
                constants.alert_db.find({"mail": mail}))
            if all_alert:
                constants.alert_db.delete_many({"mail": mail})

            return {"mail": mail, "password": password}
    except Exception:
        raise
    else:
        raise HTTPException(status_code=404, detail="Wrong User or password")


# To get all alert
# GET /alert/


@app.get("/alert/", response_model=List[methods.Alert])
async def get_my_alert(mail: str, password: str):
    try:
        return methods.alerts_entity(
            constants.alert_db.find({"mail": mail, "password": password}))
    except Exception:
        raise HTTPException(status_code=404, detail="ERROR")


# To post an alert
# POST /alert/


@app.post("/alert/", response_model=methods.Alert)
async def create_alert(
        mail: str, password: str, currency: str, price: int, method: str
):
    try:
        if not (method == "above" or method == "below"):
            raise methods.MethodError

        if not methods.is_valid_currency(currency):
            raise methods.CurrencyError

        password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        query = {"mail": mail, "password": password}
        if not methods.users_entity(
                constants.userlist_db.find(query)):
            raise methods.UserNotFoundError

        alert = {"mail": mail, "currency": currency,
                 "price": price, "method": method}
        constants.alert_db.insert_one(alert)
        return alert

    except methods.UserNotFoundError:
        raise HTTPException(status_code=404,
                            detail="User not found in database")

    except methods.MethodError:
        raise HTTPException(
            status_code=404,
            detail="Wrong syntax method, method should be 'below' or 'above'",
        )

    except methods.CurrencyError:
        raise HTTPException(
            status_code=404,
            detail="Crypto currency is not available on COINS-API"
        )

    except methods.CoinApiError:
        url = "https://rest.coinapi.io/v1/assets"
        headers = constants.COIN_API_KEY
        response = methods.requests.get(url, headers=headers)

        raise HTTPException(
            status_code=404,
            detail=f"There is a problem with COINS-API, "
                   f"code error :{response.status_code}",
        )

    except Exception:
        raise HTTPException(status_code=404, detail="error")


# To delete particular alert
# DELETE /alert/


@app.delete("/alert/", response_model=methods.Alert)
async def delete_alert(
        mail: str, password: str, currency: str, price: int, method: str
):
    try:
        password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        query = {"mail": mail, "password": password}
        if not methods.users_entity(
                constants.userlist_db.find(query)):
            raise methods.UserNotFoundError

        alert = {"mail": mail, "currency": currency,
                 "price": price, "method": method}
        if constants.alert_db.find(alert)[0]:
            constants.alert_db.delete_one(alert)
            return alert
        else:
            raise methods.AlertError

    except methods.UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except methods.AlertError:
        raise HTTPException(status_code=404, detail="Alert do not exist")
    except Exception:
        raise HTTPException(status_code=404, detail="error")
