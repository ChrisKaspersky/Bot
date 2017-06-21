import logging #Библиотека для ведения логов, потом пригодится
import vk.exceptions #Модуль с описанием исключений связанных с API
import time
import requests.packages.urllib3.exceptions
import requests.exceptions
from datetime import datetime

logging.basicConfig(format='[# %(levelname)-10s [%(asctime)s]  %(message)s', level=logging.INFO)

tokenfile = open('token.txt','r')
noanswer=open('noanswers.txt','w')
quests={'привет':'Привет.','дела':'Хорошо, как у тебя?'}


def finder(message):
    message2 = message
    message = message.replace('?','')
    answer = ""
    message=message.split(' ')
    for word in message:
        try:
            answer=answer + ' ' + quests[word]
        except KeyError:
            continue
    if answer.replace(' ','') == "":
        noanswer.write(message2+'\n')
        answer = 'И все таки я такого не знаю'
    return answer


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
    api = vk.API(session) #Создаём обьект класса API
    log("Соединение установлено")
except vk.exceptions.VkAuthError: # Если ошибка заключается в авторизации
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
            api.messages.send(user_id=last_message[1]['uid'], message=finder(last_message[1]['body']))
            sender = api.users.get(user_ids=last_message[1]['uid'])[0]['first_name'] + ' ' + api.users.get(user_ids=last_message[1]['uid'])[0]['last_name']
            log('('+ sender + ')' + "Сообщение принято: " + last_message[1]['body'])
            log('('+ sender + ')' + "Сообщение отправлено: " + finder(last_message[1]['body']))
        time.sleep(2)
    except requests.packages.urllib3.exceptions.ReadTimeoutError or requests.exceptions.ReadTimeout:
        log("Соединение разорвано, попытка подключения")
        try:
            session = vk.Session(access_token=token)
            api = vk.API(session)
            log("Соединение установлено")
        except vk.exceptions.VkAuthError:
            log("Авторизация не удалась: неверный токен")
            raise vk.exceptions.AUTHORIZATION_FAILED
#