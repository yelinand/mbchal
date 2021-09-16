FROM ubuntu:latest

USER root

RUN apt-get update
RUN apt-get install -y nginx && \
    apt-get install -y python3-pip && \
    apt-get install -y python-is-python3


ADD mbchal.py requirements.txt .
RUN pip install -r requirements.txt

RUN python mbchal.py
RUN cp mbchal.html /var/www/html/index.html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]