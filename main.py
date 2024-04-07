from datetime import datetime

import requests
from pythonping import ping
import argparse
from speedtest import Speedtest
from threading import Thread
import logging

parser = argparse.ArgumentParser()

parser.add_argument(
    '-t', '--token', help='Telegram BOT Token', type=str)
parser.add_argument(
    '-c', '--chatid', help='Telegram Chat ID', type=str)

args = parser.parse_args()


hosts = ('192.168.1.1', '192.168.1.201', '192.168.1.202', '192.168.1.203', '192.168.1.204', '192.168.1.250',
         '192.168.1.251')
telegram_url = f'https://api.telegram.org/bot{args.token}/sendMessage'
data = {
    'chat_id': args.chatid,
    'text': ''
}
ping_count = 4
datetime_now = str(datetime.now().strftime('%m/%d/%Y %H:%M'))


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


def ping_host(host):
    ping_result = ping(host, count=15, timeout=1)
    return {
        'avg_latency': ping_result.rtt_avg_ms,
        'min_latency': ping_result.rtt_min_ms,
        'max_latency': ping_result.rtt_max_ms,
        'packet_loss': ping_result.packet_loss
    }


def speedtest_daily():
    """
    Speedtest daily
    """
    if datetime_now[-5:] in ['07:00', '13:00', '18:00', '21:00']:
        s = Speedtest()
        s.download()
        s.upload()
        results = s.results.dict()
        my_server = str(results['server']['host']).split(':')[0]
        results.update(ping_host(my_server))
        mes = f'======= {datetime_now} =======\nServer: {my_server}\nISP: {results["server"]["sponsor"]}\nCountry: {results["server"]["country"]}\nDownload: {results["download"] // 10e5}\nUpload: {results["upload"] // 10e5}\nPing: {results["ping"]}\nAvg Latency: {results["avg_latency"]}\nPacket Loss: {round(results["packet_loss"], 2)}'
        logging.info(mes)
        data['text'] = mes
        send_telegram()


if __name__ == '__main__':
    while True:
        t1 = Thread(target=check_routers)
        t2 = Thread(target=speedtest_daily)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
