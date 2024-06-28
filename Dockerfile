FROM python:3.12.4-slim

LABEL name="TikTokDownloader" version="5.4 Beta" authors="JoeanAmier"

COPY src /src
COPY static /static
COPY templates /templates
COPY license /license
COPY main.py /main.py
COPY requirements.txt /requirements.txt

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

CMD ["python", "main.py"]
