FROM python:3.13-slim

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app

RUN pip install -r requirements.txt

# RUN pipのインストール/pipでFlaskのインストール/FlaskAlchmy
# RUN sqlliteのインストール