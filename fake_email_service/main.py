from fastapi import FastAPI
from pydantic import BaseModel


class EmailSchema(BaseModel):
    subject: str
    body: str
    from_email: str
    to_email: str


app = FastAPI()


@app.get("/health")
def healthcheck():
    return {"status": "ok"}


@app.post("/email")
def send_email(email: EmailSchema):
    print(email.body)
    return {"message": f"Email sent to {email.to_email}"}


@app.post("/email/slow")
def send_email_slow(email: EmailSchema):
    import time

    time.sleep(30)
    return {"message": f"Email sent to {email.to_email}"}


@app.post("/email/error")
def send_email_error(email: EmailSchema):
    raise Exception("Error sending email")
