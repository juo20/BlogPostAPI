FROM python:3.9.7

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

ARG DATABASE_HOSTNAME
ARG DATABASE_PORT
ARG DATABASE_PASSWORD
ARG DATABASE_NAME
ARG DATABASE_USERNAME
ARG SECRET_KEY
ARG ALGORITHM
ARG ACCESS_TOKEN_EXPIRE_MINUTES
ARG PORT

ENV PORT ${PORT}

EXPOSE $PORT

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT}"]