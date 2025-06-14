FROM python:3.11-slim

COPY app /app
COPY requirements/app.txt /requirements.txt

RUN pip install -r /requirements.txt
RUN mkdir models

WORKDIR /app
ENV PYTHONPATH="/"

CMD ["python", "main.py"]
