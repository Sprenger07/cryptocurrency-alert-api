from pydantic import BaseModel
import re
import requests

import constants


class MailError(Exception):
    pass


class PasswordError(Exception):
    pass


class UserExistError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class MethodError(Exception):
    pass


class CurrencyError(Exception):
    pass


class AlertError(Exception):
    pass


class CoinApiError(Exception):
    pass


class Alert(BaseModel):
    mail: str
    currency: str
    price: int
    method: str


def alert_entity(item) -> dict:
    return {
        "mail": str(item["mail"]),
        "currency": str(item["currency"]),
        "price": int(item["price"]),
        "method": str(item["method"]),
    }


def alerts_entity(entity) -> list:
    return [alert_entity(item) for item in entity]


# ===================================================#


class User(BaseModel):
    mail: str
    password: str


def user_entity(item) -> dict:
    return {"mail": str(item["mail"]), "password": str(item["password"])}


def users_entity(entity) -> list:
    return [user_entity(items) for items in entity]


def is_valid_mail(mail):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    return re.fullmatch(regex, mail)


def is_valid_password(password):
    regex = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
    return re.fullmatch(regex, password)


def is_valid_currency(currency):
    url = f"https://rest.coinapi.io/v1/assets/{currency}"
    headers = constants.COIN_API_KEY
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise CoinApiError

    return response.content != b"[]"
