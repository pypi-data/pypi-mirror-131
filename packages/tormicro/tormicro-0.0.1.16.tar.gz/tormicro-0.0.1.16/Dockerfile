FROM python:3-slim

ADD sources.list /etc/apt/sources.list

RUN buildDeps='gcc libc6-dev make' && \
    set -x && \
    apt-get update && apt-get install -y $buildDeps --no-install-recommends && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple tormicro==0.0.1.15 && \
    mkdir /app && \
    apt-get purge -y --auto-remove $buildDeps

WORKDIR /app

ENTRYPOINT [ "tormicro" ]
CMD [ "-h" ]