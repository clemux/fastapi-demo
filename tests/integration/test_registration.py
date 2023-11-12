def test_register_and_activate(client, capsys):
    response_register = client.post(
        "/users/", json={"email": "user@example.com", "password": "password"}
    )
    assert response_register.status_code == 200
    assert response_register.json() == {"message": "User created: user@example.com"}

    captured = capsys.readouterr()
    code = captured.out.strip()

    response = client.post(
        "/users/me/activate",
        auth=("user@example.com", "password"),
        json={
            "code": code,
        },
    )
    assert response.status_code == 200
    assert response.json() == {"message": "User activated"}


def test_post_users_with_email_service_error(
    app, override_settings_email_error, client
):
    response = client.post(
        "/users/", json={"email": "user@example.com", "password": "password"}
    )
    assert response.status_code == 500


def test_post_users_with_email_service_timeout(
    app, override_settings_email_slow, client
):
    response = client.post(
        "/users/", json={"email": "user@example.com", "password": "password"}
    )
    assert response.status_code == 500
