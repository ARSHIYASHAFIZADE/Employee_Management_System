from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from pydantic import BaseModel, EmailStr

class EmployeeCreate(BaseModel):
    employee_id: str = Field(..., min_length=3, max_length=20, example="EMP123")
    name: str = Field(..., min_length=1, max_length=100, example="John Doe")
    age: int = Field(..., ge=18, le=60, example=30)
    department: str = Field(..., min_length=1, max_length=50, example="Engineering")
    
    @field_validator('created_at', 'updated_at', check_fields=False)
    def prevent_timestamp_override(cls, v):
        raise ValueError('Timestamps are auto-generated and cannot be set manually')

class EmployeeResponse(BaseModel):
    employee_id: str
    name: str
    age: int
    department: str

class BulkEmployeeResponse(BaseModel):
    inserted: int
    skipped: int
    details: List[str] 
    
    class Config:
        from_attributes = True

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: Optional[str] = "user"    

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
