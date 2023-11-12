"""User routes."""
import logging.config
import uuid
from typing import Annotated

from aiomysql import Connection
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.hash import pbkdf2_sha256

from app.config import Settings, get_settings
from app.dependencies import get_current_user, get_db
from app.exceptions import (
    EmailAlreadyExistsException,
    EmailServiceError,
    InvalidActivationCodeException,
)
from app.lib.email import EmailBackend
from app.lib.users import insert_user, activate_user, insert_activation_code
from app.lib.utils import generate_activation_code
from app.schemas.user import (
    UserCreateSchema,
    UserSchema,
    UserActivateSchema,
    MessageResponseSchema,
    ErrorResponseSchema,
)

router = APIRouter()

logger = logging.getLogger()


@router.post(
    "/users/",
    response_model=MessageResponseSchema,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
    },
)
async def user_registration(
    user: UserCreateSchema,
    db: Annotated[Connection, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
):
    """User registration endpoint."""
    password_hash = pbkdf2_sha256.hash(user.password)
    user_id = uuid.uuid4()
    user = UserSchema(
        id=user_id, email=user.email, password=password_hash, activated=False
    )
    async with db.cursor() as cursor:
        try:
            await insert_user(cursor, user)
        except EmailAlreadyExistsException as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
            ) from exc

        code = generate_activation_code()
        await insert_activation_code(
            cursor,
            user,
            code,
            settings.code_expiration_seconds,
        )

        email_backend = EmailBackend(
            settings.email_service_base_url,
            settings.email_service_endpoint,
            settings.email_service_timeout_seconds,
        )
        try:
            await email_backend.send_email(
                "Activation code",
                body=code,
                from_email=settings.from_email,
                to_email=user.email,
            )
        except EmailServiceError as exc:
            logger.error(
                "Could not connect to the email service",
            )
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Email service error",
            ) from exc
    await db.commit()
    logger.info("User created", extra={"user": user.email})
    return {"message": f"User created: {user.email}"}


@router.post(
    "/users/me/activate",
    response_model=MessageResponseSchema,
    responses={
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponseSchema},
        status.HTTP_409_CONFLICT: {"model": ErrorResponseSchema},
    },
)
async def user_activation(
    activated_user: UserActivateSchema,
    db: Annotated[Connection, Depends(get_db)],
    current_user: Annotated[UserSchema, Depends(get_current_user)],
):
    """User activation endpoint."""
    if current_user.activated:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already activated",
        )
    async with db.cursor() as cursor:
        try:
            await activate_user(cursor, current_user, activated_user.code)
        except InvalidActivationCodeException:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid activation code",
            )
    await db.commit()
    logger.info("User activated", extra={"user": current_user.email})
    return {"message": "User activated"}
