FROM python:3.8-alpine

COPY requirements.txt requirements.txt
RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
RUN pip install -r requirements.txt

COPY app.py app.py
COPY aws.py aws.py
COPY models.py models.py
COPY response.py response.py
COPY templates templates
COPY static static

#arguments as env variables
ARG ARG_REDWOOD_SECRET_KEY
ENV REDWOOD_SECRET_KEY ${ARG_REDWOOD_SECRET_KEY}

EXPOSE 8080

CMD [ "python3", "app.py" ]
