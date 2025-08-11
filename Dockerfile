FROM python:3.9-slim

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    pip install -r requirements.txt

WORKDIR /app
COPY app .

CMD ["python", "app.py"]
