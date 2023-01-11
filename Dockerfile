# Basic flask container

FROM fanoftal2/flask-crud-base:1

COPY app /root
WORKDIR /root

# ENTRYPOINT ["python3", "app.py"]