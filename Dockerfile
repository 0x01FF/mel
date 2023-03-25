# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR .

RUN apt-get update && apt-get upgrade -y


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN apt-get install ffmpeg libsm6 libxext6 espeak -y

COPY . .

CMD [ "python3", "-u", "bot.py"]