import logging
import vk.exceptions
import time
import requests.exceptions
from response import *
from datetime import datetime

logging.basicConfig(format='[# %(levelname)-10s [%(asctime)s]  %(message)s', level=logging.INFO)

tokenfile = open('token.txt','r')


def log(information):
	logs = open('logs.txt', 'a')
	logging.info(information)
	time = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M")
	writable_information = time + ": " + information.lower() +'\n'
	logs.write(writable_information)
	logs.close()


log("Сервис запущен") # Вывод инфы по авторизации
log("Авторизация...")
token=tokenfile.readline()

try:
	session = vk.Session(access_token=token)
	api = vk.API(session)
	log("Соединение установлено")
except vk.exceptions.VkAuthError:
	log("Авторизация не удалась: неверный токен")
	raise vk.exceptions.AUTHORIZATION_FAILED

log("Начат приём сообщений")

last_message = ''
while True:
	try:
		last_message=api.messages.get(out=0,count=1)
		last_message[1]['body']=last_message[1]['body'].lower()
		the_lastest_message=api.messages.getHistory(count=1, user_id=last_message[1]['uid'])
		the_lastest_message[1]['body']=the_lastest_message[1]['body'].lower()
		if (the_lastest_message[1]['body']==last_message[1]['body']) and (the_lastest_message[1]['uid']!=434145659):
			api.messages.send(user_id=last_message[1]['uid'], message=respond(last_message[1]['body']))
			our_message=api.messages.get(out=1,count=1)
			if our_message[1]['body']=='И все таки я такого не знаю':
				noanswer=open('noanswers.txt','a')
				noanswer.write(str(last_message[1]['body'])+'\n')
				noanswer.close()
			sender = api.users.get(user_ids=last_message[1]['uid'])[0]['first_name'] + ' ' + api.users.get(user_ids=last_message[1]['uid'])[0]['last_name']
			log('('+ sender + ')' + "Сообщение принято: " + last_message[1]['body'])
			log('('+ sender + ')' + "Сообщение отправлено: " + respond(last_message[1]['body']))
		time.sleep(2)
	except requests.exceptions.ReadTimeout :
		log("Соединение разорвано, попытка подключения")
		try:
			session = vk.Session(access_token=token)
			api = vk.API(session)
			log("Соединение установлено")
		except vk.exceptions.VkAuthError:
			log("Авторизация не удалась: неверный токен")
			raise vk.exceptions.AUTHORIZATION_FAILED