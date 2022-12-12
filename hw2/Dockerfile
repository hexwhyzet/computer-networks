FROM python:3.10-slim

RUN apt-get update -y
RUN apt-get install -y iputils-ping

COPY main.py .

ENTRYPOINT ["python3", "main.py"]