from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models import (Users, Employees, user_pydantics, user_pydantic_employee, 
                    user_pydantic_employees, user_pydantic_employee_registration)
from hashing import Hash
from tokens import Token
from users import GetUser


router = APIRouter(tags=['Attendence Management'])


@router.post('/token')
async def generate_token(request_form: OAuth2PasswordRequestForm = Depends()):
    try:
        token = await Token.token_generator(request_form.username, request_form.password)
        return {"access_token" : token, "token_type" : "bearer"}
    except Exception as error:
        return {"error" : str(error)}
    
@router.post('/employee-registration')
async def employee_registration(user:user_pydantics, employee:user_pydantic_employee_registration):
    try:
        user_info = user.dict(exclude_unset = True)
        employee_info = employee.dict(exclude_unset = True)
        user_info['password'] = Hash.get_hashed_password(user_info['password'])
        user_obj = await Users.create(**user_info)
        emp_obj = await Employees.create(**employee_info, employee=user_obj)
        return {"status" : "ok", "message" : "Employee registered successfully"}
    except Exception as error:
        return {"error" : str(error)}

@router.get('/get-all-employee')
async def get_all_employees():
    try:
        response = await user_pydantic_employees.from_queryset(Employees.all())
        return {"status" : "ok", "data" : response}
    except Exception as error:
        return {"error" : str(error)}

@router.get('/get-employee/{id}')
async def get_employee(employee_number: str):
    try:
        employee = await Employees.get(employee_number = employee_number)
        return {"status" : "ok", 
                "data" : 
                    {
                        "employee_number" : employee.employee_number,
                        "employee_name" : employee.employee_name,
                        "employee_status" : employee.employee_status,
                    
                    }
                }
    except Exception as error:
        return {"error" : str(error)}

@router.put('/edit-employee/{id}')
async def update_employee(employee_number: str, update_info : user_pydantic_employee, user: user_pydantics = Depends(GetUser.get_current_user)):
    try:
        employee = await Employees.get(employee_number = employee_number)
        update_info = update_info.dict(exclude_unset=True)  
        employee = await employee.update_from_dict(update_info)
        await employee.save()
        response = await user_pydantic_employee.from_tortoise_orm(employee)
        return {'status' : 'ok', "data" : response}
    except Exception as error:
        return {"error" : str(error)}

@router.delete("/delete-employee/{id}")
async def delete_employee(employee_number: str, user: user_pydantics = Depends(GetUser.get_current_user)):
    try:
        employee = await Employees.get(employee_number = employee_number)
        user = await Users.get(id=employee.id)
        await employee.delete()
        await user.delete()
        return {"status" : "ok", "message" : "employee deleted successfully"}
    except Exception as error:
        return {"error" : str(error)}
    