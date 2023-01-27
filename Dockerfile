# Basic flask container

# FROM fanoftal2/flask-crud-base:1
# FROM nikolaik/python-nodejs
# FROM ubuntu/nginx
FROM cseelye/ubuntu-nginx-uwsgi-flask

EXPOSE 5000
COPY app /root
WORKDIR /root

RUN apt-get update
RUN apt-get -y install python3
RUN apt-get -y install gcc
RUN apt-get update
# RUN apt-get -y install build-essensial
RUN apt-get -y install python3-pip
RUN pip install --user -r requirements.txt
RUN cp flask_server /etc/nginx/sites-enabled/

# ENTRYPOINT["gunicorn", "-b", "0.0.0.0:8000", "app:app"]