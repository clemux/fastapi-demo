"""Email client."""

import httpx
from httpx import TimeoutException, ConnectError

from app.exceptions import EmailServiceError


class EmailBackend:
    """Email client."""

    def __init__(self, base_url: str, endpoint: str, timeout_seconds: int):
        self.base_url = base_url
        self.endpoint = endpoint
        self.timeout_seconds = timeout_seconds

    async def send_email(self, subject, body, from_email, to_email):
        """Send email to a single recipient."""
        url = self.base_url + self.endpoint
        async with httpx.AsyncClient() as client:
            try:
                r = await client.post(
                    url,
                    json={
                        "subject": subject,
                        "body": body,
                        "from_email": from_email,
                        "to_email": to_email,
                    },
                    timeout=self.timeout_seconds,
                )
            except (TimeoutException, ConnectError) as exc:
                raise EmailServiceError from exc
        if r.status_code >= 400:
            raise EmailServiceError
        print(body)
