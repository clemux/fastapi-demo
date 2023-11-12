import pytest
from freezegun import freeze_time

from app.config import Settings


def test_post_users(client, httpx_mock):
    settings = Settings()
    httpx_mock.add_response(
        url=f"{settings.email_service_base_url}{settings.email_service_endpoint}",
        method="POST",
    )
    response = client.post(
        "/users/", json={"email": "user@example.com", "password": "password"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "User created: user@example.com"}


@pytest.mark.anyio
async def test_post_users_with_existing_email_should_return_400(async_client, user):
    response = await async_client.post(
        "/users/", json={"email": "user@example.com", "password": "password"}
    )
    assert response.status_code == 400


@pytest.mark.anyio
@freeze_time("2023-11-14 00:00:01")
async def test_post_activate(client, user, activation_code):
    response = client.post(
        "/users/me/activate",
        auth=("user@example.com", "password"),
        json={
            "code": "2812",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"message": "User activated"}


@pytest.mark.anyio
@freeze_time("2023-11-14 00:00:01")
async def test_post_activate_with_user_already_activated_should_return_409(
    client,
    user_activated,
):
    response = client.post(
        "/users/me/activate",
        auth=("user@example.com", "password"),
        json={
            "code": "2812",
        },
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "User already activated"}


def test_post_activate_with_wrong_password_should_return_401(client, user):
    response = client.post(
        "/users/me/activate",
        auth=("user@example.com", "wrong_password"),
        json={
            "code": "1234",
        },
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


def test_post_activate_with_unknown_user_should_return_401(client, user):
    response = client.post(
        "/users/me/activate",
        auth=("unknown@example.com", "wrong_password"),
        json={
            "code": "1234",
        },
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


@pytest.mark.anyio
async def test_post_activate_with_wrong_code_should_return_403(
    client, user, activation_code
):
    response = client.post(
        "/users/me/activate",
        auth=("user@example.com", "password"),
        json={
            "code": "4000",
        },
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid activation code"}


@pytest.mark.anyio
@freeze_time("2023-11-14 00:01:01")
async def test_post_activate_with_expired_code_should_return_403(
    client, user, activation_code
):
    response = client.post(
        "/users/me/activate",
        auth=("user@example.com", "password"),
        json={
            "code": "2812",
        },
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid activation code"}
