from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional


class UserCreate(BaseModel):
    name:     str
    email:    EmailStr
    password: str
    phone:    Optional[str] = None

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("كلمة المرور يجب أن تكون 8 أحرف على الأقل")
        return v


class UserUpdate(BaseModel):
    name:    Optional[str] = None
    phone:   Optional[str] = None
    address: Optional[str] = None
    avatar:  Optional[str] = None


class UserOut(BaseModel):
    id:         int
    name:       str
    email:      str
    phone:      Optional[str]
    avatar:     Optional[str]
    address:    Optional[str]
    is_admin:   bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ChangePassword(BaseModel):
    current_password: str
    new_password:     str

    @field_validator("new_password")
    @classmethod
    def check_len(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("كلمة المرور الجديدة يجب أن تكون 8 أحرف على الأقل")
        return v
