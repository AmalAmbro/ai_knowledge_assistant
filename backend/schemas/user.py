from pydantic import BaseModel, EmailStr, StrictBool

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int

    class Confing:
        from_attributes = True
