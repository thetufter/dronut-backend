FROM python:3.8-bullseye
EXPOSE 8000
WORKDIR /backend
COPY requirements.txt /backend
RUN python3 -m pip install -r requirements.txt --no-cache-dir
COPY . /backend