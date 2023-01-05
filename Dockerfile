FROM python:3.11.0

RUN pip install --no-cache-dir requests

COPY . .

CMD [ "python", "/main.py"]