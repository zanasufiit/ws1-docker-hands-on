FROM python:3.8.1-slim-buster

RUN apt-get update && apt-get install -y \
    tini \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

ENTRYPOINT [ "tini", "-g", "--" ]
CMD ["python", "app.py"]
