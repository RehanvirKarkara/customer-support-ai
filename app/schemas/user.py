from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum

class CustomerType(str, Enum):
    PREPAID = "PREPAID"
    POSTPAID = "POSTPAID"
    BROADBAND = "BROADBAND"
    DTH = "DTH"


class UserCreate(BaseModel):
    customer_id: str = Field(..., min_length=5, max_length=20)
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    phone_number: str = Field(..., min_length=10, max_length=15)
    customer_type: CustomerType


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    customer_type: Optional[CustomerType] = None


class UserResponse(BaseModel):
    id: int
    customer_id: str
    full_name: str
    email: EmailStr
    phone_number: str
    customer_type: CustomerType
    is_active: bool

    model_config = {
        "from_attributes": True
    }
    
class Token(BaseModel):
    access_token: str
    token_type: str