from fastapi import FastAPI, APIRouter, HTTPException, status
from config import collection
from database.schemas import all_employees, single_employee
from database.models import EmployeeCreate, EmployeeResponse
from datetime import datetime
from typing import List

app = FastAPI()
router = APIRouter(prefix="/employees", tags=["Employees"])

@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(employee_id: str):
    employee = collection.find_one({"employee_id": employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return single_employee(employee)

@router.get('/', response_model=List[EmployeeResponse])
async def get_all_employees():
    employees = list(collection.find())
    return all_employees(employees)  
    
@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(new_employee: EmployeeCreate):

    if collection.find_one({"employee_id": new_employee.employee_id}):
        raise HTTPException(
            status_code=400,
            detail="Employee ID already exists"
        )

    employee_data = new_employee.model_dump()
    now = datetime.now().timestamp()
    employee_data.update({
        'created_at': now,
        'updated_at': now
    })
    
    result = collection.insert_one(employee_data)
    return EmployeeResponse(**employee_data)

@router.put("/{employee_id}", response_model=EmployeeResponse)
async def update_employee(employee_id: str, updated_employee: EmployeeCreate):
    existing = collection.find_one({"employee_id": employee_id})
    if not existing:
        raise HTTPException(
            status_code=404,
            detail=f"Employee with id {employee_id} not found"
        )
    
    update_data = updated_employee.dict(exclude={"employee_id"})
    update_data['updated_at'] = datetime.now().timestamp()
    
    result = collection.update_one(
        {"employee_id": employee_id},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=400,
            detail="No changes were made"
        )

    updated_doc = collection.find_one({"employee_id": employee_id})
    return EmployeeResponse(**updated_doc)

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: str):
    result = collection.delete_one({"employee_id": employee_id})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Employee with id {employee_id} not found"
        )
   

app.include_router(router)