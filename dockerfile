FROM python:3.11-slim
WORKDIR /Owner-avatar-Proga-po-katologu-music-album-main
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "run.py"]