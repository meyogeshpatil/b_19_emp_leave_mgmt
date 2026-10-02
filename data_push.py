import requests
import random
import names
# response = requests.get('https://spotter-august-awaken.ngrok-free.dev/employees')
# print(response)
# print(response.json())


def get_dept():
    dept = ['engineering', 'it', 'finance', 'marketing', 'sales', 'hr']
    return random.choice(dept)

def get_role():
    role = ['emp', 'mgr']
    return random.choice(role)

def get_gender():
    gender = ['male', 'female']
    return random.choice(gender)

def get_names():
    gnd = get_gender()
    return names.get_first_name(gender=gnd), names.get_last_name()

for _ in range(523, 10_00):
    dept = get_dept()
    role = get_role()
    first_name, last_name = get_names()
    data = {
        "first_name": first_name.lower(),
        "last_name": last_name.lower(),
        "department": dept,
        "role": role
        }
    response = requests.post('https://spotter-august-awaken.ngrok-free.dev/employees', json=data)
    print(response.status_code)

