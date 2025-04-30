FROM python:3.11-slim

WORKDIR /app

COPY wallpapers.py .

RUN pip install --no-cache-dir pillow

ENTRYPOINT ["python", "wallpapers.py"]
CMD ["--input", "/data/wallpapers", "--output", "/data/sorted"]