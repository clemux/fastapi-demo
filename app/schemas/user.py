"""User schemas."""
import uuid

from pydantic import BaseModel, Field


class UserCreateSchema(BaseModel):
    """Schema for the registering endpoint's request body."""

    email: str = Field(example="user@example.com")
    password: str = Field(example="MyVeryStrongP@assword!")


class UserActivateSchema(BaseModel):
    """Schema for the activation endpoint's request body."""

    code: int = Field(example=1234)


class UserSchema(BaseModel):
    """Represents a user in the database."""

    id: uuid.UUID = Field()
    email: str = Field(example="user@example.com")
    activated: bool = Field(example=True)
    password: str = Field()
