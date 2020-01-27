FROM python:3.8-alpine3.11

COPY ./setup.py /app/setup.py

RUN pip install /app/

WORKDIR /app/

EXPOSE 8080

CMD ["python", "-m", "pipelines.api"]