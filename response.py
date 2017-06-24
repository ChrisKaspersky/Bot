import random

question_words = ["как","когда","где","зачем","кто"]
statements = [["привет","хай","здравствуй"]]


def requesttype(message):
	message = message.lower().split(" ")
	if (message.count("?") >= 1) or (message[0] in question_words):
		return 1
	else:
		return 0
# 1 - Вопрос
# 0 - Утверждение


def statement(message):
	answer = ""
	for word in message.split(' '):
		for i in range(len(statements)):
			if word in statements[i]:
				answer = random.sample(statements[i],1)[0]
				break
	if answer == "":
		answer = "Извини, я не понял о чём ты"
	return answer


def question(message):
	return "Я пока что не умею отвечать на вопросы"


def respond(message):
	if requesttype(message) == 1:
		answer = question(message)
	else:
		answer = statement(message)
	return answer
