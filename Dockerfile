FROM python:3.13.0a4-slim-bullseye

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip3 install --only-binary=:all: -r requirements.txt

COPY main.py .

CMD [ "python3", "/main.py"]
