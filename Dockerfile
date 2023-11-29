# action will be executed in a python3 container
FROM python:3.13.0a2-slim-bullseye

# copy requirements.txt to the container
COPY requirements.txt /requirements.txt

# install dependencies
RUN apt-get update -y && \
    apt install --fix-broken && \
    apt-get install build-essential libssl-dev libffi-dev python-dev python3-dev && \
    pip install --upgrade pip && \
    pip install -r /requirements.txt

# copy main.py to the container
COPY main.py /main.py

# run main.py
CMD [ "python", "/main.py"]