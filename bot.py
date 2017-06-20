import logging #Библиотека для ведения логов, потом пригодится
import vk.exceptions #Модуль с описанием исключений связанных с API
import time

logging.basicConfig(format='[# %(levelname)-10s [%(asctime)s]  %(message)s', level=logging.INFO)

tokenfile=open('token.txt','r')
#/////logss=open('loggs.txt','w')

quest=['Привет','привет','Как дела?','как дела?','Как дела','как дела']
ans=['Привет','Привет','Хорошо, как у тебя?','Хорошо, как у тебя','Хорошо, как у тебя','Хорошо, как у тебя','Хорошо, как у тебя','Хорошо, как у тебя']

def answer(vopr):
	for i in range (0,len(quest)+1):
		if i==len(quest):
			break
		if vopr==quest[i]:
			return ans[i]
	if i==len(quest):
		return 'Я не знаю такого вопроса'

logging.info("Сервис запущен") # Вывод инфы по авторизации
logging.info("Авторизация...")
token=tokenfile.readline()

try:
    session = vk.Session(access_token=token)
    api = vk.API(session) #Создаём обьект класса API
except vk.exceptions.VkAuthError: # Если ошибка заключается в авторизации
        logging.info('Авторизация не удалась: неверный логин или пароль')

logging.info("Начат приём сообщений")

last_message = ''
while True:													#*
	if last_message != api.messages.get(out=0,count=1):
		last_message = api.messages.get(out=0,count=1)
		#usser=users.get(user_ids=last_message[1]['uid'])['first_name']
		print(last_message[1]['body'])

		api.messages.send(user_id=last_message[1]['uid'], message=answer(last_message[1]['body'])) #Отправка ответа
	time.sleep(1)											#*

