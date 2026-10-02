from db import get_connection
from psycopg2.extras import RealDictCursor
import string
import random
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError, InvalidHashError
import jwt 
from datetime import datetime, timedelta, timezone

pwd_hasher = PasswordHasher()

jwt_sceret = 'my_secret_key'
jwt_alg = 'HS256'
jwt_expire_minutes = 15
jwt_issuer = 'leave_mgmt'
jwt_audience = 'leave_mgmt_api'


def create_name(f_name, l_name):
    return f'{f_name.capitalize()} {l_name.capitalize()}'

def get_email_ids(f_name, l_name):
    query_sql = f'''
    SELECT
        email
    From 
        employees
    where 
        name = '{create_name(f_name, l_name)}'
    '''
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query_sql)
    result = cur.fetchall()
    return [i[0] for i in result]

# version = cur.fetchone()[0]
def create_email_id(f_name, l_name):
    email_ids = get_email_ids(f_name, l_name)
    if email_ids and len(email_ids)>=1:
        if len(email_ids) == 1:
            return f'{f_name}.1.{l_name}@abc.com'
        return f'{f_name}.{int(email_ids[-1].split('.')[1])+1}.{l_name}@abc.com'
    else:
        return f'{f_name}.{l_name}@abc.com'

def generate_password():
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    spcial_characters = '!@#$%&'
    digits = string.digits
    chars = uppercase + lowercase + spcial_characters + digits
    pwd = [random.choice(chars) for _ in range(12)]
    return ''.join(pwd)


def hash_pwd(pwd):
    return pwd_hasher.hash(pwd)

def verify_pwd(pwd, h_pwd):
    try:
        return pwd_hasher.verify(h_pwd, pwd)
    except(
        VerifyMismatchError,
        VerificationError,
        InvalidHashError
    ):
        return False

def create_token(emp_id, email, role):
    now = datetime.now(timezone.utc)
    payload = dict (sub = str(emp_id), email = email, role = role, iss = jwt_issuer, aud = jwt_audience, iat = now, exp = now + timedelta(minutes=jwt_expire_minutes))
    token = jwt.encode(payload, jwt_sceret, algorithm= jwt_alg)
    return token


def decode_token(token : str):
    payload = jwt.decode(token, jwt_sceret, algorithms= [jwt_alg,], issuer= jwt_issuer, audience= jwt_audience)
    return payload

def get_department(emp_id):
    query_sql = '''
    SELECT
        department
    From 
        employees
    where 
        employee_id = %s
    '''
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query_sql, (emp_id,))
    result = cur.fetchone()
    return result[0]
