from pydantic import BaseModel

class Alert(BaseModel):
    mail : str
    currency : str
    price : int
    method : str


def alertEntity(item) -> dict:
    return {
        "mail" : str(item["mail"]),
        "currency" : str(item["currency"]),
        "price" : int(item["price"]),
        "method" : str(item["method"])
    }

def alertsEntity(entity) -> list:
    return [alertEntity(item) for item in entity]


#===================================================#

class User(BaseModel):
    mail : str
    password : str

def userEntity(item) -> dict:
    return {
        "mail" : str(item["mail"]),
        "password" : str(item["password"])
    }

def usersEntity(entity) -> list:
    return [userEntity(items) for items in entity]