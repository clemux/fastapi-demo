"""User schemas."""
import uuid

from pydantic import BaseModel, Field, EmailStr


class UserCreateSchema(BaseModel):
    """Schema for the registering endpoint's request body."""

    email: EmailStr = Field(
        json_schema_extra={
            "example": "user@example.com",
        }
    )
    password: str = Field(
        json_schema_extra={
            "example": "MyVeryStrongP@assword!",
        }
    )


class UserActivateSchema(BaseModel):
    """Schema for the activation endpoint's request body."""

    code: str = Field(json_schema_extra={"example": "1234"})


class UserSchema(BaseModel):
    """Represents a user in the database."""

    id: uuid.UUID = Field()
    email: EmailStr
    activated: bool
    password: str = Field()


class EmailAlreadyExistsResponseSchema(BaseModel):
    """Schema for the error response when the email already exists."""

    detail: str


class MessageResponseSchema(BaseModel):
    """Generic response with a message"""

    message: str = Field(json_schema_extra={"example": "User created"})


class ErrorResponseSchema(BaseModel):
    """Generic response for errors"""

    detail: str = Field(json_schema_extra={"example": "User already exists"})
