# for run
import os
# bottle stuff
from bottle import run, request, get, post

@post("/bot") #процедура (или функция, хз), отвечающая за работу бота; находится по адресу [твойсайт]/bot
def sendtxt():
    text = 'Hello' #какой текст будем отсылать
    token = '308406795:AAGUJZuSykK1DuZnQHF1GVEr0lU6BT-DMjU' #токен твоего бота (чата с ботом) - надо в ботмастере получить, вроде
    chatid = request.json['message']['chat']['id'] #из json берем массив "message", в нём находим элемент "chat", и оттуда берём "id" - идентификатор нашего чата
    requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s..' %(token, chatid, text)) #собираем ссылку из трех строк (см выше), и делаем на неё get-запрос
    print(request.json) #в логи (heroku logs) выводим всю инфу по get-запросу (собственно, json - и есть словарь, содержащий всю эту инфу)