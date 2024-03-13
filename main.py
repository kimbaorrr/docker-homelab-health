import datetime

import requests
from pythonping import ping
import argparse
 
parser = argparse.ArgumentParser()
 
parser.add_argument("-t", "--token", help = "Telegram BOT Token")
parser.add_argument("-c", "--chatid", help = "Telegram Chat ID")

args = parser.parse_args()

HOSTS = ('192.168.1.1', '192.168.1.249', '192.168.1.250', '192.168.1.251', '192.168.1.252', '192.168.1.253',
         '192.168.1.254')
DNS = ('greencloud-sgn-1.edge.nextdns.io', 'greencloud-han-1.edge.nextdns.io', 'dns.google')
TELEGRAM_BOT_TOKEN = args.token 
TELEGRAM_CHAT_ID = args.chatid
TELEGRAM_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
DATA = {
	'chat_id': TELEGRAM_CHAT_ID,
	'text': ''
}
COUNT = 5

def send_telegram():
	res = requests.post(TELEGRAM_URL,data=DATA)
	if res.status_code != 200:
		message = f'Không thể gửi tin nhắn vào lúc {str(datetime.datetime.now())} do Server bị mất Internet hoặc Telegram down!'
		print(message)

def check_routers():
	for host in HOSTS:
		if not ping(host, count=COUNT).success():
			mes = f"Router {host} is down !"
			print(mes)
			DATA['text'] = mes
			send_telegram()

def check_dns():
	for dns in DNS:
		if not ping(dns, count=COUNT).success():
			mes = f"DNS {dns} is down !"
			print(mes)
			DATA['text'] = mes
			send_telegram()

if __name__ == '__main__':
	while True:
		check_routers()
		check_dns()
