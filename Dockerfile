FROM python:alpine3.7
RUN apk update && apk upgrade
RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev openssl-dev libffi-dev
COPY . /app
WORKDIR /app
RUN chmod 755 /app/webscrapper.py /app/wind_tracker.py /app/telegram_bot.py /app/consts.py /app/windInfo.py
RUN pip install -r /app/requirements.txt
RUN /usr/bin/crontab /app/crontab.txt
CMD ["sh", "-c", "crond && python /app/telegram_bot.py"]