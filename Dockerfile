# Basic flask container

# FROM fanoftal2/flask-crud-base:1
FROM nikolaik/python-nodejs

EXPOSE 5000
COPY app /root
WORKDIR /root

RUN pip install -r requirements.txt
# RUN cd /root
# CMD ["python", "/root/tools/txt_2_PostgreSql.py"]

# ENTRYPOINT ["python", "/root/tools/txt_2_PostgreSql.py"]