FROM python:alpine3.7
ARG BOT_TOKEN
ARG WIND_ALERT_GROUP_CHAT_ID
ARG FIREBASE_ENV
ARG CLIENT_EMAIL
ARG CLIENT_ID
ARG CLIENT_X509_CERT_URL
ARG PRIVATE_KEY
ARG PRIVATE_KEY_ID
ARG PROJECT_ID
RUN apk update && apk upgrade
RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev openssl-dev libffi-dev
COPY . /app
WORKDIR /app
# if build is being automated from docker hub, then secrests.json.secret does not exist, we create is using build env variables
RUN if [ ! -f secrests.json.secret ]; then echo -e "{\n \"_comment\" : \"JSON Doc from EV - For AutoBuild\",\n\"bot_token\" : \"${BOT_TOKEN}\",\n \"wind_alert_group_chat_id\" : \"${WIND_ALERT_GROUP_CHAT_ID}\"\n}" > secrests.json.secret; fi
RUN if [ ! -f wind-info-firebase-adminsdk-tfxe3-aa9146d5b8.json.secret ]; then echo ${FIREBASE_ENV} > wind-info-firebase-adminsdk-tfxe3-aa9146d5b8.json.secret; fi
RUN chmod 755 /app/webscrapper.py /app/wind_tracker.py /app/telegram_bot.py /app/consts.py /app/windInfo.py /app/run.sh
RUN pip install -r /app/requirements.txt
RUN /usr/bin/crontab /app/crontab.txt
#RUN touch /etc/profile.d/envs.sh
#RUN echo "export BOT_TOKEN=${bot_token}" >> /etc/profile.d/envs.sh
#RUN echo "export WIND_ALERT_GROUP_CHAT_ID=${wind_alert_group_chat_id}" >> /etc/profile.d/envs.sh
#RUN chmod +x /etc/profile.d/envs.sh
CMD ["sh", "-c", "crond && python /app/telegram_bot.py"]