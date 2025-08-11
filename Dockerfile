FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    pip install yt-dlp flask redis

WORKDIR /app
COPY app .

CMD ["python", "app.py"]
