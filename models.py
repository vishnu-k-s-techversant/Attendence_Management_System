from tortoise import Model,fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Users(Model):
    username = fields.CharField(max_length=20, null=False, unique=True)
    password = fields.CharField(max_length=100, null=False)

    def __str__(self):
        return self.username


class Employees(Model):
    employee = fields.ForeignKeyField('models.Users', on_delete=fields.CASCADE)
    employee_number = fields.CharField(max_length=20, null=False, unique=True)
    employee_name = fields.CharField(max_length=20, null=False)
    date = fields.DateField(auto_now_add=True)
    employee_status = fields.CharField(max_length=20, null=False, default='Not in yet')

    def __str__(self):
        return self.employee_number
    
    
user_pydantics = pydantic_model_creator(Users, name='User', exclude={'id'})

user_pydantic_employee_registration = pydantic_model_creator(Employees, 
                name='EmployeeRegistration', exclude={'id', 'employee'})

user_pydantic_employee = pydantic_model_creator(Employees, 
                name='EmployeeIn', exclude={'id', 'date'})

user_pydantic_employees = pydantic_model_creator(Employees, 
                name='Employees')
