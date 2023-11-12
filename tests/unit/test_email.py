import httpx
import pytest

from app.exceptions import EmailServiceError
from app.lib.email import EmailBackend


@pytest.mark.anyio
async def test_send_email(httpx_mock, capsys):
    httpx_mock.add_response(url="http://example.com/email", method="POST", json={})
    backend = EmailBackend("http://example.com", "/email", 5)
    await backend.send_email(
        "Activation code", "1234", "app@example.com", "user@example.com"
    )
    captured = capsys.readouterr()
    assert "1234" in captured.out


@pytest.mark.anyio
async def test_send_email_with_error(httpx_mock):
    httpx_mock.add_response(
        url="http://example.com/email", method="POST", json={}, status_code=500
    )
    backend = EmailBackend("http://example.com", "/email", 5)
    with pytest.raises(EmailServiceError):
        await backend.send_email(
            "Activation code", "1234", "app@example.com", "user@example.com"
        )


@pytest.mark.anyio
async def test_send_email_with_timeout(httpx_mock):
    httpx_mock.add_exception(httpx.ReadTimeout("Unable to read within timeout"))
    backend = EmailBackend("http://example/email", "/email", 1)
    with pytest.raises(EmailServiceError):
        await backend.send_email(
            "Activation code", "1234", "app@example.com", "user@example.com"
        )
