FROM python:3.6.9-slim-stretch

WORKDIR /home/python/app

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 3000

CMD python application.py