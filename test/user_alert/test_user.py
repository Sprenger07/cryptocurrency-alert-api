import requests

# REGISTER
# POST METHOD

def test_user_create():
    mail = "test_new_user@gmail.com"
    password = "abcd1234"
    response = requests.post(f"http://localhost:8000/user/?mail={mail}&password={password}")
    assert (response.status_code == 200)


def test_user_already_exist():
    mail = "test_new_user@gmail.com"
    password = "abcd1234"
    response = requests.post(f"http://localhost:8000/user/?mail={mail}&password={password}")
    assert (response.status_code == 404)


def test_user_missing_at():
    mail = "test_new_user1gmail.com"
    password = "abcd1234"
    response = requests.post(f"http://localhost:8000/user/?mail={mail}&password={password}")
    assert (response.status_code == 404)


def test_user_missing_extension():
    mail = "test_new_user2@gmail"
    password = "abcd1234"
    response = requests.post(f"http://localhost:8000/user/?mail={mail}&password={password}")
    assert (response.status_code == 404)


def test_user_wrong_extension():
    mail = "test_new_user3@gmail.gmail"
    password = "abcd1234"
    response = requests.post(f"http://localhost:8000/user/?mail={mail}&password={password}")
    assert (response.status_code == 404)


def test_user_short_password():
    mail = "test_new_user4@gmail.com"
    password = "abc"
    response = requests.post(f"http://localhost:8000/user/?mail={mail}&password={password}")
    assert (response.status_code == 404)


def test_user_missing_number_in_password():
    mail = "test_new_user5@gmail.com"
    password = "abcdABCD"
    response = requests.post(f"http://localhost:8000/user/?mail={mail}&password={password}")
    assert (response.status_code == 404)


def test_user_missing_letter():
    mail = "test_new_user6@gmail.com"
    password = "12341234"
    response = requests.post(f"http://localhost:8000/user/?mail={mail}&password={password}")
    assert (response.status_code == 404)


# LOGIN
# GET METHOD

def test_user_login():
    mail = "test_new_user@gmail.com"
    password = "abcd1234"
    response = requests.get(f"http://localhost:8000/user/?mail={mail}&password={password}")
    assert (response.status_code == 200)


def test_user_no_exist():
    mail = "test_new_do_not_exist@gmail.com"
    password = "abcd1234"
    response = requests.get(f"http://localhost:8000/user/?mail={mail}&password={password}")
    assert (response.status_code == 404)

# CHANGE PASSWORD
# PUT METHOD


def test_user_change_password():
    mail = "test_new_user@gmail.com"
    password = "abcd1234"
    new_password = "1234abcd"
    response = requests.put(f"http://localhost:8000/user/?mail={mail}&old_password={password}&new_password={new_password}")
    assert (response.status_code == 200)


def test_user_change_password_2():
    mail = "test_new_user@gmail.com"
    password = "1234abcd"
    new_password = "abcd1234"
    response = requests.put(f"http://localhost:8000/user/?mail={mail}&old_password={password}&new_password={new_password}")
    assert (response.status_code == 200)


def test_user_change_wrong_password():
    mail = "test_new_user@gmail.com"
    password = "abcd1234"
    new_password = "abcd1234"
    response = requests.put(f"http://localhost:8000/user/?mail={mail}&old_password={password}&new_password={new_password}")
    assert (response.status_code == 404)


def test_user_change_not_valid_password():
    mail = "test_new_user@gmail.com"
    password = "abcd1234"
    new_password = "abcd"
    response = requests.put(f"http://localhost:8000/user/?mail={mail}&old_password={password}&new_password={new_password}")
    assert (response.status_code == 404)

# DELETE USER
# DELETE METHOD


def test_user_delete():
    mail = "test_new_user@gmail.com"
    password = "abcd1234"
    response = requests.delete(f"http://localhost:8000/user/?mail={mail}&password={password}")
    assert (response.status_code == 200)


def test_user_delete_second_time():
    mail = "test_new_user@gmail.com"
    password = "abcd1234"
    response = requests.delete(f"http://localhost:8000/user/?mail={mail}&password={password}")
    assert (response.status_code == 404)


def test_user_delete_wrong_password():
    mail = "test_new_user@gmail.com"
    password = "abcd"
    response = requests.delete(f"http://localhost:8000/user/?mail={mail}&password={password}")
    assert (response.status_code == 404)


def test_user_delete_1():
    mail = "test_new_user1gmail.com"
    password = "abcd1234"
    response = requests.delete(f"http://localhost:8000/user/?mail={mail}&password={password}")
    assert (response.status_code == 404)


def test_user_delete_2():
    mail = "test_new_user2@gmail"
    password = "abcd1234"
    response = requests.delete(f"http://localhost:8000/user/?mail={mail}&password={password}")
    assert (response.status_code == 404)


def test_user_delete_3():
    mail = "test_new_user3@gmail.gmail"
    password = "abcd1234"
    response = requests.delete(f"http://localhost:8000/user/?mail={mail}&password={password}")
    assert (response.status_code == 404)


def test_user_delete_4():
    mail = "test_new_user4@gmail.com"
    password = "abc"
    response = requests.delete(f"http://localhost:8000/user/?mail={mail}&password={password}")
    assert (response.status_code == 404)


def test_user_delete_5():
    mail = "test_new_user5@gmail.com"
    password = "abcdABCD"
    response = requests.delete(f"http://localhost:8000/user/?mail={mail}&password={password}")
    assert (response.status_code == 404)


def test_user_delete_6():
    mail = "test_new_user6@gmail.com"
    password = "12341234"
    response = requests.delete(f"http://localhost:8000/user/?mail={mail}&password={password}")
    assert (response.status_code == 404)



