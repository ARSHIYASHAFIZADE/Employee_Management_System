def single_employee(employee):
    return {
        "employee_id": str(employee["employee_id"]),
        "name": employee["name"],
        "age": employee["age"],
        "department": employee["department"]
    }
    
def all_employees(employees):
    return [single_employee(employee) for employee in employees]
