import logging #Библиотека для ведения логов, потом пригодится
import vk.exceptions #Модуль с описанием исключений связанных с API
import time
from datetime import datetime

logging.basicConfig(format='[# %(levelname)-10s [%(asctime)s]  %(message)s', level=logging.INFO)

tokenfile = open('token.txt','r')

quest = ['Привет','привет','Как дела?','как дела?','Как дела','как дела']
ans = ['Привет','Привет','Хорошо, как у тебя?','Хорошо, как у тебя','Хорошо, как у тебя','Хорошо, как у тебя','Хорошо, как у тебя','Хорошо, как у тебя']


def log(information): #Функция для вывода информации в консоль и автоматической дозаписи лога
    logs = open('logs.txt', 'a')
    logging.info(information)
    time = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M")
    writable_information = time + ": " + information.lower() +'\n'
    logs.write(writable_information)
    logs.close()


def answer(vopr):
    for i in range (0,len(quest)+1):
        if i==len(quest):
            break
        if vopr==quest[i]:
            return ans[i]
    if i==len(quest):
        return 'Я не знаю такого вопроса'


log("Сервис запущен") # Вывод инфы по авторизации
log("Авторизация...")
token=tokenfile.readline()

try:
    session = vk.Session(access_token=token)
    api = vk.API(session) #Создаём обьект класса API
except vk.exceptions.VkAuthError: # Если ошибка заключается в авторизации
        log('Авторизация не удалась: неверный токен')
        raise vk.exceptions.AUTHORIZATION_FAILED

log("Начат приём сообщений")

last_message = api.messages.get(out=0, count=1)
while True:
    print(last_message)
    print(api.messages.get(out=0, count=1))
    if last_message[1]['body'] != api.messages.get(out=0, count=1)[1]['body']:
        last_message = api.messages.get(out=0, count=1)
        #user=users.get(user_ids=last_message[1]['uid'])['first_name']
        log("принято сообщение: " + last_message[1]['body'])

        api.messages.send(user_id=last_message[1]['uid'], message=answer(last_message[1]['body'])) #Отправка ответа
        time.sleep(1)
    time.sleep(1)

