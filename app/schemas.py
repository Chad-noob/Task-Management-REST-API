from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

TaskStatus = Literal['pending', 'in_progress', 'completed']


class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)

    @field_validator('name')
    @classmethod
    def clean_name(cls, value: str) -> str:
        return value.strip()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)


class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = Field(default='', max_length=1000)
    status: TaskStatus = 'pending'

    @field_validator('title')
    @classmethod
    def clean_title(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError('Title cannot be empty or only spaces')
        return cleaned

    @field_validator('description')
    @classmethod
    def clean_description(cls, value: Optional[str]) -> str:
        return (value or '').strip()


class TaskStatusUpdateRequest(BaseModel):
    status: TaskStatus


class UserData(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime


class TaskData(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatus
    created_at: datetime
