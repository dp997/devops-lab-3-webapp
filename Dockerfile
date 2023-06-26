FROM ubuntu:22.04

RUN apt-get update && \
    apt-get -y install python3.10 pip

RUN mkdir /app

COPY app.py /app/app.py

COPY requirements.txt /app/requirements.txt

ADD templates /app/templates

WORKDIR /app/

RUN pip3 install -r requirements.txt 

EXPOSE 80

CMD python3.10 app.py
