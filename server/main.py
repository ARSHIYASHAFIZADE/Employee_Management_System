import csv
import io
from fastapi import FastAPI, APIRouter, HTTPException, status
from config import collection
from database.schemas import all_employees, single_employee
from database.models import EmployeeCreate, EmployeeResponse, BulkEmployeeResponse, UserRegister, UserLogin, TokenResponse
from datetime import datetime
from typing import List
from fastapi import File, UploadFile, Depends, HTTPException
from auth import users_collection, verify_password, create_access_token, get_current_user
import os
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

@router.post("/import", response_model=BulkEmployeeResponse)
async def import_employees(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    content = await file.read()
    csv_data = io.StringIO(content.decode("utf-8"))
    reader = csv.DictReader(csv_data)

    inserted = 0
    skipped = 0
    details = []

    for row in reader:
        employee_id = row.get("employee_id")
        if not employee_id:
            skipped += 1
            details.append("Missing employee_id in row")
            continue

        if collection.find_one({"employee_id": employee_id}):
            skipped += 1
            details.append(f"Employee ID {employee_id} already exists")
            continue

        employee_data = {
            "employee_id": row["employee_id"],
            "name": row["name"],
            "age": int(row["age"]),
            "department": row["department"],
            "created_at": datetime.now().timestamp(),
            "updated_at": datetime.now().timestamp()
        }

        collection.insert_one(employee_data)
        inserted += 1

    return BulkEmployeeResponse(inserted=inserted, skipped=skipped, details=details)

@router.post("/auth/login", response_model=TokenResponse)
def login(user: UserLogin):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/users/me")
def read_users_me(current_user=Depends(get_current_user)):
    return {"email": current_user["email"]}


app.include_router(router)