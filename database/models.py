from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional

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
    
    class Config:

        from_attributes = True
