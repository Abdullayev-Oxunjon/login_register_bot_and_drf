import requests

BASE_URL = 'http://127.0.0.1:8000/api/v1'


def register_user_to_api(username, phone_number, password):
    URL = f'{BASE_URL}/register/'
    data = {
        'username': username,
        'phone_number': phone_number,
        'password': password,
    }
    response = requests.post(URL, json=data)
    return response


def login_user_to_api(phone_number, password):
    URL = f'{BASE_URL}/login/'
    data = {
        'phone_number': phone_number,
        'password': password,
    }
    response = requests.post(URL, json=data)
    return response
