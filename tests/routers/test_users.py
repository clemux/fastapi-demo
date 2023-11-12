import pytest
from freezegun import freeze_time


def test_post_users(client):
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
    print(response)
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


def test_post_activate_with_wrong_password_should_return_401(client):
    response = client.post(
        "/users/me/activate",
        auth=("user@example.com", "wrong_password"),
        json={
            "code": "1234",
        },
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"
