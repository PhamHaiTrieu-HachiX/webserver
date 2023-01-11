# Basic flask container

# FROM fanoftal2/flask-crud-base:1
FROM nikolaik/python-nodejs

COPY app /root
WORKDIR /root

# RUN apt-get update
# RUN apt-get -y install pip
# RUN apt-get -y install nodejs
# RUN apt-get -y install npm
RUN pip install -r requirements.txt

# ENTRYPOINT ["python3", "app.py"]