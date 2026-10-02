from pydantic import BaseModel, Field, field_validator
import re

class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    department: str
    role: str

    @field_validator('first_name')
    @classmethod
    def validate_first_name(cls, value):
        if not re.fullmatch(r'^[a-z]{1,35}$', value):
            raise ValueError('First Name must be in capital letter. Digits, speical characters are not allowed in the name. e.g. JOHN')
        return value

    @field_validator('last_name')
    @classmethod
    def validate_last_name(cls, value):
        if not re.fullmatch(r'^[a-z]{1,35}$', value):
            raise ValueError('Last Name must be in capital letter. Digits, speical characters are not allowed in the name. e.g. JOHN')
        return value

    @field_validator('department')
    @classmethod
    def validate_department(cls, value):
        if value.lower() not in ['engineering', 'finance', 'it', 'sales', 'marketing', 'hr']:
            raise ValueError(f'Department {value} should be any of these. engineering/finance/it.')
        return value

    @field_validator('role')
    @classmethod
    def validate_role(cls, value):
        if value.lower() not in ['emp', 'mgr']:
            raise ValueError('Role {role.lower()} shoule be like, emp/mgr.')
        return value


class EmployeeLogin(BaseModel):
    username : str
    pwd : str