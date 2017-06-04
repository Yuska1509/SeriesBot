# -*- coding: utf-8 -*-
# for run
import os
import json
import requests
import progfile
import bdserials
from datetime import datetime, date
from bottle import run, request, get, post, static_file


a = progfile.db()


b = a.fetch('select sname from Serials')
dic = {"keyboard": b}
keyboard = json.dumps(dic)


sspisok = ''
for i in range(len(b)):
    c = str(b[i])
    c = c[2:-3]
    sspisok = sspisok+'\n'+c


@get("/notify")
def notify():
#    da1 = date(2017, 3, 20)
    da = datetime.today()
    da1 = datetime.date(da)
    da = int(datetime.toordinal(da1))
    sendinfo=a.fetch('SELECT Podpiski.uid, Episodes.sname, Episodes.ename from Episodes inner join Podpiski on Podpiski.sid = Episodes.sid where (Episodes.date+Podpiski.status) = %d;' %da)
    token = '308210124:AAHkb6qVLTqo0pIKsn_IQTZqvYJ7wpzVJn0'
    for i in sendinfo:
        text = "Today (%s) you can watch \'%s\' of \'%s\'. Have a good day!" %(da1, i[2], i[1])
        chat_id = i[0]
        requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s' % (token, chat_id, text))


@post("/")
def ListOfSerials():
    token = '308210124:AAHkb6qVLTqo0pIKsn_IQTZqvYJ7wpzVJn0'
    chat_id = request.json['message']['chat']['id']
    tetext = request.json['message']['text']  # text which user wrote

@get('/filedownload')
def stat_file():
    return static_file('serials.db', root=".", download=True)

run(host="0.0.0.0", port=os.environ.get('PORT', 5000))

