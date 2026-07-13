from enum import Enum
from pydantic import BaseModel, EmailStr, Field


# -------------------------
# Enums
# -------------------------

class ServiceType(str, Enum):
    PREPAID = "PREPAID"
    POSTPAID = "POSTPAID"
    BROADBAND = "BROADBAND"
    DTH = "DTH"
    AIRTEL_BLACK = "AIRTEL_BLACK"


class CustomerType(str, Enum):
    REGULAR = "REGULAR"
    PREMIUM = "PREMIUM"
    VIP = "VIP"


# -------------------------
# Register
# -------------------------

class UserCreate(BaseModel):
    customer_id: str = Field(..., min_length=5, max_length=20)
    full_name: str
    email: EmailStr
    password: str = Field(..., min_length=8)

    mobile_number: str

    service_type: ServiceType

    customer_type: CustomerType = CustomerType.REGULAR

    preferred_language: str = "English"

    circle: str


# -------------------------
# Login
# -------------------------

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# -------------------------
# Response
# -------------------------

class UserResponse(BaseModel):
    id: int
    customer_id: str
    full_name: str
    email: EmailStr

    mobile_number: str

    service_type: ServiceType

    customer_type: CustomerType

    preferred_language: str

    circle: str

    is_active: bool

    model_config = {
        "from_attributes": True
    }


# -------------------------
# JWT Token
# -------------------------

class Token(BaseModel):
    access_token: str
    token_type: str