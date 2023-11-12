FROM python:3.10

USER root
RUN useradd -ms /bin/bash dailymotion

COPY ./requirements.txt /opt/fastapi-demo/requirements.txt
COPY ./requirements-dev.txt /opt/fastapi-demo/requirements-dev.txt

COPY ./app /opt/fastapi-demo/app

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /opt/fastapi-demo
RUN pip install --upgrade --no-cache-dir pip==23.3.1 && pip install --no-cache-dir -r requirements.txt


USER dailymotion

CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080"]
