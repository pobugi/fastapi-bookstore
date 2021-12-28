FROM python:3.9 as build

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /

COPY poetry.lock pyproject.toml /

RUN pip install poetry poetry-core virtualenv && \
    poetry export --output requirements.txt --without-hashes --with-credentials && \
    python -m virtualenv venv && \
    ./venv/bin/pip install --compile --no-cache-dir --global-option=build_ext --global-option="-j 4" -r requirements.txt

RUN find / -name libkeyutils.so.1

FROM python:3.9-slim-buster as run

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/code \
    PORT=8000

WORKDIR /code

COPY --from=build /venv/ /venv

RUN apt-get update && \
    apt-get -y install netcat && \
    apt-get clean && \
    /venv/bin/pip install psycopg2-binary==2.9.1

COPY app ./app
COPY alembic ./alembic
COPY alembic.ini entrypoint.sh poetry.lock pyproject.toml .env ./

RUN chmod +x /code/entrypoint.sh

EXPOSE $PORT

ENTRYPOINT ["/code/entrypoint.sh"]
CMD /venv/bin/uvicorn app.main:app --host 0.0.0.0 --port $PORT --ws none
