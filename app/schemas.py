from datetime import datetime
from pydantic import BaseModel, field_validator


class UserCreate(BaseModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def username_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError("Username не может быть пустым")
        return value.strip()

    @field_validator("password")
    @classmethod
    def password_min_length(cls, value):
        if len(value) < 6:
            raise ValueError("Пароль должен содержать минимум 6 символов")
        return value


class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str