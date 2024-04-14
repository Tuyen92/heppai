import json
from dataclasses import dataclass

@dataclass
class Employee:
    name: str
    profile: str

def json_to_employee(json_string: str):
    data_dict = json.loads(json_string)

    employees = [Employee(**employee_data) for employee_data in data_dict]
    
    return employees

