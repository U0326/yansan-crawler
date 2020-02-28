FROM python:3.8.0a3-alpine3.9

RUN apk update
RUN apk add build-base libffi-dev libxml2-dev libxslt-dev
ENV TZ JST-9

ENV YOUTUBE_API_KEY change_it
COPY ./ /opt/yansan-crawler/
COPY ./crontab /var/spool/cron/crontabs/root
WORKDIR /opt/yansan-crawler
RUN pip install --upgrade pip
RUN pip install -r ./require.txt

CMD sh ./assets/docker_bootstrap.sh
