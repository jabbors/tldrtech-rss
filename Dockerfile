FROM python:3.11.7-alpine3.19

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY *.py /app

CMD python run.py