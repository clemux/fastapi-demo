"""User routes."""

import uuid
from typing import Annotated

from aiomysql import Connection
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.hash import pbkdf2_sha256

from app.dependencies import get_current_user, get_db
from app.exceptions import EmailAlreadyExistsException
from app.lib.users import insert_user, activate_user
from app.schemas.user import UserCreateSchema, UserSchema, UserActivateSchema

router = APIRouter()


@router.post("/users/")
async def user_registration(
    user: UserCreateSchema, db: Annotated[Connection, Depends(get_db)]
):
    """User registration endpoint."""
    password_hash = pbkdf2_sha256.hash(user.password)
    user_id = uuid.uuid4()
    user = UserSchema(
        id=user_id, email=user.email, password=password_hash, activated=False
    )
    try:
        await insert_user(db, user)
    except EmailAlreadyExistsException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        ) from exc

    return {"message": f"User created: {user.email}"}


@router.post("/users/me/activate")
async def user_activation(
    activated_user: UserActivateSchema,
    db: Annotated[Connection, Depends(get_db)],
    current_user: Annotated[UserSchema, Depends(get_current_user)],
):
    """User activation endpoint."""
    if await activate_user(db, current_user, activated_user.code):
        return {"message": "User activated"}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid activation code"
    )
