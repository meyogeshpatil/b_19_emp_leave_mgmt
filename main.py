from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from psycopg2.extras import RealDictCursor

from schema import EmployeeCreate, EmployeeLogin
from db import get_db
from utility import create_name, create_email_id, generate_password, hash_pwd, verify_pwd, create_token, decode_token, get_department
app = FastAPI()

pwd_1001 =  'WDlZA2X2WsrS'

@app.get('/health')
def health():
    return {'msg': 'Application is running.'}


@app.middleware('http')
async def jwt_auth_middlewaare(
    request: Request,
    call_next   
):  
    public_paths = [
        '/login',
        '/docs',
        '/openapi.json'
    ]
    if request.url.path in public_paths:
            return await call_next(request)

    if not request.headers.get('authorization'):
        return JSONResponse(
            status_code = 401,
            content = {'detail': 'Authorization token is missing.'}
        )
    return await call_next(request)

@app.post('/login')
def login(payload: EmployeeLogin,  db = Depends(get_db)):
    username = payload.username
    pwd = payload.pwd
    query = '''
    select employee_id, password, role from employees where email = %s
    '''
    cursor = db.cursor()
    cursor.execute(query, (username, ))
    result = cursor.fetchone()
    if result is None:
        raise HTTPException(
            status_code= 404,
            detail= 'username does not exist.'
        )
    emp_id, h_pwd, role = result
    if verify_pwd(pwd, h_pwd):
        token = create_token(emp_id, username, role)
        return {'msg': 'login successfull', 'access_token': token}
    else:
        raise HTTPException(
                    status_code= 401,
                    detail= 'Invalid Password.'
        )


@app.get('/employees')
def get_employees(request: Request, department:str | None = None, page: int = 10, limit: int = 1, order_column: str = 'employee_id', order_by: str = 'asc',  db = Depends(get_db)):
    cursor = db.cursor(cursor_factory = RealDictCursor)
    offset = (limit - 1)*10
    if department:
        query = 'select * from employees where department = %s'
        cursor.execute(query, (department, ))
    else:
        query = f'select * from employees order by {order_column} {order_by} limit %s offset %s'
        cursor.execute(query, (page, offset))
    result = cursor.fetchall()
    return result

@app.get('/search_employee')
def get_employees_name(name:str, db = Depends(get_db)):
    cursor = db.cursor(cursor_factory = RealDictCursor)
    query = ''' select * from employees where name ilike %s '''
    cursor.execute(query, (f'%{name}%', ))
    result = cursor.fetchall()
    return result

@app.get('/employees/{employee_id}')
def get_employees_with_id(employee_id : int, db = Depends(get_db)):
    cursor = db.cursor(cursor_factory = RealDictCursor)
    query = 'select * from employees where employee_id = %s'
    cursor.execute(query, (employee_id,))
    result = cursor.fetchone()
    print(result)
    return result


@app.post('/employees')
def create_employee(
    request : Request,
    employee: EmployeeCreate,
    db= Depends(get_db)
):
    token = request.headers.get('authorization').split(' ')[-1]
    response = decode_token(token)
    dept = get_department(int(response['sub']))
    if dept == 'hr':
        pwd = generate_password()
        email = create_email_id(employee.first_name, employee.last_name)
        cursor = db.cursor()
        query = '''
        insert into employees
        (name, email, department, role, password)
        VALUES  
        (%s, %s, %s, %s, %s)
        '''
        cursor.execute(
            query,
            (
                create_name(employee.first_name, employee.last_name),
                email,
                employee.department,
                employee.role,
                hash_pwd(pwd)

            )
        )
        db.commit()

        return {
            'msg': 'Employee Created Successfully.',
            'emp_email_id': email,
            'emp_pwd': pwd
        }
    else:
        raise HTTPException(
                    status_code= 403,
                    detail= 'You dont have access to register the employee.'
        )