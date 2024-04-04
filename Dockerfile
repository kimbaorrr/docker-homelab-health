FROM python:3.12-alpine

ENV telegram_bot_token=""
ENV telegram_chat_id=""

WORKDIR /app

COPY requirements.txt ./
COPY main.py ./

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "./main.py", "-t ${telegram_bot_token} -c ${telegram_chat_id}"]