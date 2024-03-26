FROM python:3.11-alpine

WORKDIR /usr/app/src

ENV telegram_bot_token=""
ENV telegram_chat_id=""

COPY main.py ./

RUN pip install pythonping requests argparse speedtest
CMD [ "python", "-u", "./main.py -t ${telegram_bot_token} -c ${telegram_chat_id}"]