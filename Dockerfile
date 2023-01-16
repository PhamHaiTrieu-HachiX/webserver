# Basic flask container

# FROM fanoftal2/flask-crud-base:1
FROM nikolaik/python-nodejs

EXPOSE 5000
COPY app /root
WORKDIR /root

RUN pip install -r requirements.txt
RUN apt-get -y install nginx