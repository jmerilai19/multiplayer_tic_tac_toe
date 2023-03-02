# syntax=docker/dockerfile:1

FROM python:3.10-slim
WORKDIR /server
COPY game.py /server/game.py
COPY server.py /server/server.py
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
CMD [ "python3", "-m" , "flask", "--app", "server",  "run", "--host=0.0.0.0"]
