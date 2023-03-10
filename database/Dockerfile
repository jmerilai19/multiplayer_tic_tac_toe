# syntax=docker/dockerfile:1

FROM python:3.10-slim
WORKDIR /database
COPY database_api.py /database/database_api.py
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
CMD [ "python3", "-m" , "flask", "--app", "database_api",  "run", "--host=0.0.0.0"]
