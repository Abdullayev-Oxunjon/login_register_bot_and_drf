import json

import requests

BASE_URL = 'http://127.0.0.1:8000/api/v1'


# BU jarayonda belgilangan login URL manziliga POST so'rovini yuborish uchun
def login_user_to_api(phone_number, password):
    URL = f'{BASE_URL}/login/'
    data = {
        'phone_number': phone_number,
        'password': password,
    }
    response = requests.post(URL, json=data)
    return response


def add_grade_student(student_id, score):
    url = f"{BASE_URL}/add-grade/"
    data = {
        "student_id": student_id,
        "score": score  # Change the order, ensure it matches the server's expected format
    }

    response = requests.post(url=url, json=data)
    return response


# Bu jarayonda esa API dan studentlarni group_id siga ko'ra filter qilib olamiz !
def get_students(group_id):
    url = f"{BASE_URL}/persons/{group_id}/"
    response = requests.get(url=url).text
    data = json.loads(response)
    return data


# Bu jarayonda esa API dan id raqamiga ko'ra studentni olamiz
def get_student_by_id(person_id):
    url = f"{BASE_URL}/person/{person_id}/"
    response = requests.get(url=url)

    if response.status_code == 200:
        data = json.loads(response.text)
        return data
    else:
        return None


# Bu jarayonda API dan studentning bahosini olamiz !
def get_student_score(student_id):
    url = f"{BASE_URL}/get-grade/{student_id}/"
    response = requests.get(url=url).text
    data = json.loads(response)
    return data


def update_grade_in_server(person_id, score):
    url = f"{BASE_URL}/update-grade/{person_id}/"
    data = {
        "score": score
    }

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return True
        else:
            print(f"Server returned a non-200 status code: {response.status_code}")
            print(response.text)  # Print the response text for debugging
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")

    return False
