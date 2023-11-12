FROM python:3.10

COPY ./fake_email_service/requirements.txt /opt/fake_email_service/requirements.txt

COPY ./fake_email_service /opt/fake_email_service

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /opt/fake_email_service
RUN pip install --upgrade --no-cache-dir pip==23.3.1 && pip install --no-cache-dir -r requirements.txt


ENV PYTHONUNBUFFERED=1
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080"]
