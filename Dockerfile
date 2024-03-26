FROM python:3.11-alpine

ENV telegram_bot_token=""
ENV telegram_chat_id=""

RUN mkdir /tmp/homelab 
WORKDIR /tmp/homelab  

ADD . /tmp/homelab/

RUN pip install -r requirements.txt
CMD [ "python", "/tmp/homelab/main.py -t ${telegram_bot_token} -c ${telegram_chat_id}"]