# REST API Cryptocurrency Alert

Here is my cryptocurrency alert api

![final_62ac952a9389eb0089a45399_711725](https://user-images.githubusercontent.com/55802491/174327793-bef1c4b0-67db-43f0-a0dc-71863a27ed0d.gif)
## Install

    pip install -r requirements.txt 
    

## Configuration

Please put your own database and your api key in the file `/src/constants.py`

![constants](https://user-images.githubusercontent.com/55802491/174245740-2c579c06-607d-438b-b2a8-a163d9cdf97b.JPG)

## Run the api in /src/

    uvicorn api:app --host localhost --port 8000
    uvicorn api_user:app --host localhost --port 8001

## Run alert

`python3 src/send_alert.py` 

![final_62ac952a9389eb0089a45399_699961](https://user-images.githubusercontent.com/55802491/174327828-618faea7-7f34-4b7b-bab1-ad269d474d99.gif)
## Documentation:

Swagger :
<br>
http://127.0.0.1:8000/docs
<br>
http://127.0.0.1:8001/docs



## Get all alert

### Request

`GET /alert/`

    curl -X 'GET' 'http://127.0.0.1:8000/alert/?mail=leo%40gmail.com' -H 'accept: application/json'

### Response
```json
[
  {
    "mail": "leo@gmail.com",
    "currency": "BTC",
    "price": 1000,
    "method": "above"
  },
  {
    "mail": "leo@gmail.com",
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
curl -X 'POST' 'http://127.0.0.1:8000/alert/?mail=leo%40gmail.com&currency=ETH&price=2000&method=below' -H 'accept: application/json' -d ''
```

### Response

```json

{
  "mail": "leo@gmail.com",
  "currency": "ETH",
  "price": 2000,
  "method": "below"
}
```

## Delete a particular alert

### Request

`DELETE /alert/`

    curl -X 'DELETE' 'http://127.0.0.1:8000/alert/?mail=leo%40gmail.com&currency=ETH&price=2000&method=below' -H 'accept: application/json'

### Response

```json

{
  "mail": "leo@gmail.com",
  "currency": "ETH",
  "price": 2000,
  "method": "below"
}

```

## Get a particular user

### Request

`GET /user/`

    curl -X 'GET' 'http://127.0.0.1:8001/user/?mail=leo%40gmail.com' -H 'accept: application/json'

### Response

```json
{
  "mail": "leo@gmail.com"
}
```

## Change password of an user

### Request

`PUT /user/`

curl -X 'PUT' 'http://127.0.0.1:8001/user/?mail=leo%40gmail.com&old_password=1234&new_password=abcd' -H 'accept: application/json'

### Response

```json
{
  "mail": "leo@gmail.com"
}
```

## Create an user

### Request

`POST /user/`

    curl -X 'POST' http://127.0.0.1:8001/user/?mail=pierre%40gmail&password=pierre' -H 'accept: application/json' -d ''

### Response

```json
{
  "mail": "pierre@gmail.com"
}
```

## Delete an user

### Request

`DELETE /user/`
  
  curl -X 'DELETE' 'http://127.0.0.1:8001/user/?mail=leo%40gmail.com&password=abcd' -H 'accept: application/json'

### Response

```json
{
  "mail": "leo@gmail.com"
}
```

## Gel all user

### Request

`GET /all_user/

    curl -X 'GET' 'http://127.0.0.1:8001/all_user/' -H 'accept: application/json'

### Response

```json
[
  {
    "mail": "paul@gmail.com"
  },
  {
    "mail": "pierre@gmail.com"
  },
  {
    "mail": "jaques@gmail.com"
  }
]


```
