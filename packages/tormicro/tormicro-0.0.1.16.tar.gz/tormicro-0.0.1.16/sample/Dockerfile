FROM registry-vpc.cn-hangzhou.aliyuncs.com/xiaomai/tormicro

ADD sources.list /etc/apt/sources.list
ADD . /app

RUN buildDeps='gcc libc6-dev make' && \
    set -x && \
    apt-get update && apt-get install -y $buildDeps --no-install-recommends && \
    rm -rf /var/lib/apt/lists/* ; \
    test -f /app/requirements.txt  && pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r /app/requirements.txt; \
    apt-get purge -y --auto-remove $buildDeps

CMD [ "tormicro" ]