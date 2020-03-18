FROM python:3.8-alpine3.11

RUN apk add --no-cache libstdc++ g++ libressl-dev musl-dev libffi-dev

COPY ./requirements /app/requirements

RUN pip install -r /app/requirements/requirements.txt

COPY ./pipelines /app/pipelines
COPY ./setup.py /app/setup.py

RUN pip install /app/

RUN apk del libressl-dev musl-dev libffi-dev

WORKDIR /app/

EXPOSE 8080

CMD ["python", "-m", "pipelines.api"]