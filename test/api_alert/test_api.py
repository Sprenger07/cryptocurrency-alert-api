import requests


# INIT
def test_init_user():
    mail = "test_new_user@gmail.com"
    password = "abcd1234"
    response = requests.post(f"http://localhost:8000/user/?mail={mail}&password={password}")
    assert (response.status_code == 200)


def get_alert():
    mail = "test_new_user@gmail.com"
    password = "abcd1234"
    response = requests.get(f"http://localhost:8000/alert/?mail={mail}&password={password}")
    assert (response.status_code == 200)


def get_alert_no_exist():
    mail = "test_new_user_no_exist@gmail.com"
    password = "abcd1234"
    response = requests.get(f"http://localhost:8000/alert/?mail={mail}&password={password}")
    assert (response.status_code == 404)


# POST
def test_post_alert():
    mail = "test_new_user@gmail.com"
    password = "abcd1234"
    currency = "BTC"
    price = 7000
    method = "below"
    response = requests.post(f"http://localhost:8000/alert/?mail={mail}&password={password}&currency={currency}&price={price}&method={method}")
    assert (response.status_code == 200)


def test_post_alert_wrong_password():
    mail = "test_new_user@gmail.com"
    password = "1234"
    currency = "BTC"
    price = 7000
    method = "below"
    response = requests.post(f"http://localhost:8000/alert/?mail={mail}&password={password}&currency={currency}&price={price}&method={method}")
    assert (response.status_code == 404)


def test_post_alert_wrong_currency():
    mail = "test_new_user@gmail.com"
    password = "abcd1234"
    currency = "NONE"
    price = 7000
    method = "below"
    response = requests.post(f"http://localhost:8000/alert/?mail={mail}&password={password}&currency={currency}&price={price}&method={method}")
    assert (response.status_code == 404)

def test_post_alert_wrong_method():
    mail = "test_new_user@gmail.com"
    password = "abcd1234"
    currency = "BTC"
    price = 7000
    method = "under"
    response = requests.post(f"http://localhost:8000/alert/?mail={mail}&password={password}&currency={currency}&price={price}&method={method}")
    assert (response.status_code == 404)


# DELETE ALERT

def test_delete_wrong_alert():
    mail = "test_new_user@gmail.com"
    password = "abcd1234"
    currency = "BTC"
    price = 800
    method = "below"
    response = requests.delete(f"http://localhost:8000/alert/?mail={mail}&password={password}&currency={currency}&price={price}&method={method}")
    assert (response.status_code == 404)


def test_delete_alert():
    mail = "test_new_user@gmail.com"
    password = "abcd1234"
    currency = "BTC"
    price = 7000
    method = "below"
    response = requests.delete(f"http://localhost:8000/alert/?mail={mail}&password={password}&currency={currency}&price={price}&method={method}")
    assert (response.status_code == 200)


def test_delete_alert_second_time():
    mail = "test_new_user@gmail.com"
    password = "abcd1234"
    currency = "BTC"
    price = 7000
    method = "below"
    response = requests.delete(f"http://localhost:8000/alert/?mail={mail}&password={password}&currency={currency}&price={price}&method={method}")
    assert (response.status_code == 404)


# DELETE USER
def test_user_delete():
    mail = "test_new_user@gmail.com"
    password = "abcd1234"
    response = requests.delete(f"http://localhost:8000/user/?mail={mail}&password={password}")
    assert (response.status_code == 200)