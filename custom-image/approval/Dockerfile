FROM python:3.9-slim
RUN pip install flask
RUN apt-get -y install procps
RUN apt-get -y install curl
ADD . ./
EXPOSE 5000