from datetime import datetime

import requests
from pythonping import ping
import argparse
from speedtest import Speedtest
from multiprocess import Process
import logging

parser = argparse.ArgumentParser()

parser.add_argument(
    "-t", "--token", help="Telegram BOT Token", type=str)
parser.add_argument(
    "-c", "--chatid", help="Telegram Chat ID", type=str)


args = parser.parse_args()

hosts = ('192.168.1.1', '192.168.1.201', '192.168.1.202', '192.168.1.203', '192.168.1.204', '192.168.1.250',
         '192.168.1.251')
telegram_url = f'https://api.telegram.org/bot{args.token}/sendMessage'
data = {
    'chat_id': args.chatid,
    'text': ''
}
ping_count = 4
datetime_now = str(datetime.now().strftime('%m/%d/%Y %H:%M:%S'))


def send_telegram():
    try:
        r = requests.post(telegram_url, data=data)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        message = f'Không thể gửi tin nhắn đến {telegram_url} vào lúc {datetime_now} !'
        logging.error(message)
        logging.error(err.response.text)


def check_routers():
    """
    Check routers
    """
    for host in hosts:
        if not ping(host, count=ping_count).success():
            mes = f"Router {host} is down !"
            logging.warning(mes)
            data['text'] = mes
            send_telegram()


def speedtest_daily():
    """
    Speedtest daily
    """
    if datetime_now[-9:-3] in ['08:00', '12:00', '19:00']:
        s = Speedtest()
        s.download()
        s.upload()
        results = s.results.dict()
        mes = f'======= {datetime_now} =======\nServer: {results["server"]["host"]}\nDownload: {int(results["download"] / 10**5)}\nUpload: {int(results["upload"] / 10**5)}\nPing: {results["ping"]}'
        logging.info(mes)
        data['text'] = mes
        send_telegram()


if __name__ == '__main__':
    while True:
        p1 = Process(target=check_routers)
        p2 = Process(target=speedtest_daily)
        p1.start()
        p2.start()
        p1.join()
        p2.join()
