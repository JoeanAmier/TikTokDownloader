FROM python:3.12.4-slim

LABEL name="TikTokDownloader" version="5.5 Beta" authors="JoeanAmier"

WORKDIR /TikTokDownloader

COPY src /TikTokDownloader/src
COPY static /TikTokDownloader/static
COPY templates /TikTokDownloader/templates
COPY license /TikTokDownloader/license
COPY main.py /TikTokDownloader/main.py
COPY requirements.txt /TikTokDownloader/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
