FROM python:3.8.1-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

EXPOSE 5000
ENTRYPOINT ["python", "app.py"]
