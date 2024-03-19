FROM python:3.12.1

WORKDIR app

COPY  . /app

RUN  sed -i 's@^.*            if self.console.input(.*$@@'  main.py &&\
     sed -i 's@^.*                    "是否已仔细阅读上述免责声明(YES/NO): ").upper() != "YES":.*$@@'  main.py &&\
     sed -i 's@^.*                return False.*$@@'  main.py &&\
     echo '/bin/bash' >> /entrypoint.sh &&\
     echo 'cd /app' >> /entrypoint.sh &&\
     echo 'echo 5 | /usr/local/bin/python main.py' >> /entrypoint.sh &&\
     chmod +x /entrypoint.sh &&\
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]