FROM python:3.11-slim

COPY service /service
COPY requirements/app.txt /requirements.txt

RUN pip install -r /requirements.txt
RUN mkdir models

WORKDIR /service
ENV PYTHONPATH="/"

CMD ["python", "app.py"]
