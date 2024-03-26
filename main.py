from datetime import datetime

import requests
from pythonping import ping
import argparse
from speedtest import Speedtest
from multiprocessing import Process

parser = argparse.ArgumentParser()

parser.add_argument("-t", "--token", help="Telegram BOT Token", type=str)
parser.add_argument("-c", "--chatid", help="Telegram Chat ID", type=str)


args = parser.parse_args()

hosts = ('192.168.1.1', '192.168.1.249', '192.168.1.250', '192.168.1.251', '192.168.1.252', '192.168.1.253',
         '192.168.1.254')
telegram_bot_token = args.token
telegram_chat_id = args.chatid
telegram_url = f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage'
data = {
    'chat_id': telegram_chat_id,
    'text': ''
}
ping_count = 4
datetime_now = str(datetime.now().strftime('%m/%d/%Y %H:%M:%S'))


def send_telegram():
    res = requests.post(telegram_url, data=data)
    if res.status_code != 200:
        message = f'Không thể gửi tin nhắn vào lúc {datetime_now} do Server bị mất Internet hoặc Telegram down!'
        print(message)

# Check routers
def check_routers():
    for host in hosts:
        if not ping(host, count=ping_count).success():
            mes = f"Router {host} is down !"
            print(mes)
            data['text'] = mes
            send_telegram()

# Speedtest daily
def speedtest_daily():
    if datetime_now[-9:-3] in ['08:00', '12:00', '19:00']:
        s = Speedtest()
        s.download()
        s.upload()
        results = s.results.dict()
        mes = f'======= {datetime_now} =======\nServer: {results["server"]["host"]}\nDownload: {round(results["download"] / 1000000, 2)}\nUpload: {round(results["upload"] / 1000000, 2)}\nPing: {results["ping"]}'
        print(mes)
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
