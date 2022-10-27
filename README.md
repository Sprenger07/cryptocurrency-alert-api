# REST API Cryptocurrency Alert

Here is my cryptocurrency alert api

![final_62ac952a9389eb0089a45399_711725](https://user-images.githubusercontent.com/55802491/174327793-bef1c4b0-67db-43f0-a0dc-71863a27ed0d.gif)
## Install

    pip install -r requirements.txt 
    

## Configuration

```sh
export MONGO_DB_SERV="mongodb://mongoAdmin:changeMe@localhost:27017"
```

Get your own private key on the website https://www.coinapi.io/

```sh
export KEY="DF0EB4B3-YOUR-API-KEY"
``` 


## Run the api in /src/
```sh
    uvicorn api:app --host localhost --port 8000
```
## Run test
```sh
pytest
```

![final_62d14257de2219008ff1fcf5_219918](https://user-images.githubusercontent.com/55802491/179208426-8eefecde-954a-40eb-bf78-094e9f277732.gif)

:warning: possible errors :
- if the user "test_new_user@gmail.com" is already in the database
- if there is an error during a request to COIN-API

## Run alert

```sh
python3 src/send_alert.py
``` 

![final_62ac952a9389eb0089a45399_699961](https://user-images.githubusercontent.com/55802491/174327828-618faea7-7f34-4b7b-bab1-ad269d474d99.gif)
## Documentation:

Swagger :
<br>
http://127.0.0.1:8000/docs


## Get all alert

### Request

`GET /alert/`

    curl -X 'GET' 'http://127.0.0.1:8000/alert/?mail=test@gmail.com&password=1234abcd@' -H 'accept: application/json'

### Response
```json
[
  {
    "mail": "test@gmail.com",
    "currency": "BTC",
    "price": 1000,
    "method": "above"
  },
  {
    "mail": "test@gmail.com",
    "currency": "BTC",
    "price": 0,
    "method": "above"
  }
]
```
## Create an alert

### Request

`POST /alert/`

```sh
curl -X 'POST' 'http://127.0.0.1:8000/alert/?mail=test@gmail.com&password=1234abcd@&currency=ETH&price=2000&method=below' -H 'accept: application/json' -d ''
```

### Response

```json

{
  "mail": "test@gmail.com",
  "currency": "ETH",
  "price": 2000,
  "method": "below"
}
```

## Delete a particular alert

### Request

`DELETE /alert/`
```sh
curl -X 'DELETE' 'http://127.0.0.1:8000/alert/?mail=test@gmail.com&password=1234abcd@&currency=ETH&price=2000&method=below' -H 'accept: application/json'
```
### Response

```json

{
  "mail": "test@gmail.com",
  "currency": "ETH",
  "price": 2000,
  "method": "below"
}

```

## Change password of an user

### Request

`PUT /user/`
```sh
curl -X 'PUT' 'http://127.0.0.1:8000/user/?mail=test@gmail.com&old_password=1234abcd@&new_password=@1234abcd' -H 'accept: application/json'
```
### Response

```json
{
  "mail": "test@gmail.com"
}
```

## Create an user

### Request

`POST /user/`
```sh
    curl -X 'POST' http://127.0.0.1:8000/user/?mail=pierre@gmail&password=pierre' -H 'accept: application/json' -d ''
```
### Response

```json
{
  "mail": "pierre@gmail.com"
}
```

## Delete an user

### Request

`DELETE /user/`
```sh
  curl -X 'DELETE' 'http://127.0.0.1:8000/user/?mail=test@gmail.com&password=1234abcd@' -H 'accept: application/json'
```
### Response

```json
{
  "mail": "leo@gmail.com"
}
```
