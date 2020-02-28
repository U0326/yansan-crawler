#!/usr/bin/env bash

cd `dirname $0`/..
sed -i -e "s/API_KEY = 'dummy_text'/API_KEY = '${YOUTUBE_API_KEY}'/" ./video/youtube/const.py
crond -f
