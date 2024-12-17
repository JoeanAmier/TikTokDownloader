FROM python:3.12-slim

LABEL name="TikTokDownloader" authors="JoeanAmier" repository="https://github.com/JoeanAmier/TikTokDownloader"

WORKDIR /TikTokDownloader

COPY src /TikTokDownloader/src
COPY locale /TikTokDownloader/locale
COPY static /TikTokDownloader/static
COPY templates /TikTokDownloader/templates
COPY license /TikTokDownloader/license
COPY main.py /TikTokDownloader/main.py
COPY requirements.txt /TikTokDownloader/requirements.txt

RUN pip install --no-cache-dir -r /TikTokDownloader/requirements.txt

VOLUME /TikTokDownloader

CMD ["python", "main.py"]
