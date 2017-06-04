# -*- coding: utf-8 -*-
# for run
import os
import json
import requests
import progfile
import bdserials
from datetime import datetime, date
from bottle import run, request, get, post, static_file
from status import StateTraveler
from bdserials import a
import req

token = '308210124:AAHkb6qVLTqo0pIKsn_IQTZqvYJ7wpzVJn0'


# @get("/notify")
# def notify():
# #   da1 = date(2017, 3, 19)
#     da = datetime.today()
#     da1 = datetime.date(da)
#     da = int(datetime.toordinal(da1))
#     sendinfo = a.fetch('SELECT Podpiski.uid, Episodes.sname, Episodes.ename, Podpiski.translation from Episodes inner join Podpiski on Podpiski.sid = Episodes.sid where (Episodes.date+Podpiski.status) = %d;' %da)
#     print("sendinfo", sendinfo)
#     token = '308210124:AAHkb6qVLTqo0pIKsn_IQTZqvYJ7wpzVJn0'
#     for i in sendinfo:
#         series = (i[1]).encode('utf-8')
#         episode = (i[2]).encode('utf-8')
#         translation = (i[3]).encode('utf-8')
#         print(series, episode, translation)
#         text = "Сегодня (%s) вы можете посмотреть серию \'%s\' сериала \'%s\' в озвучке \'%s\'" % (da1, episode, series, translation)
#         chat_id = i[0]
#         requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s' % (token, chat_id, text))


@get("/notify")
def notify():
    # da1 = date(2017, 3, 25)
    da = datetime.today()
    da1 = datetime.date(da)
    da = int(datetime.toordinal(da1))
    originalfeth = a.fetch("Select Podpiski.uid, Episodes.sname, Episodes.ename, Episodes.eid from Episodes inner join Podpiski on Podpiski.sid = Episodes.sid where (Podpiski.translation = 'Original' and Episodes.date = %d);" %da)
    print(originalfeth)
    if originalfeth != None:
        token = '308210124:AAHkb6qVLTqo0pIKsn_IQTZqvYJ7wpzVJn0'
        for i in originalfeth:
            series = (i[1]).encode('utf-8')
            episode = (i[2]).encode('utf-8')
            translation = 'Original'
            eid = i[3]
            text = "Сегодня (%s) вы можете посмотреть серию \'%s\' сериала \'%s\' в озвучке \'%s\'" % (da1, episode, series, translation)
            chat_id = i[0]
            requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s' % (token, chat_id, text))
            seriesnumber = a.fetch('Select num from Serials where sname = \'%s\'' % series)
            if seriesnumber != None:
                seriesnumber = seriesnumber[0][0]
                for elem in req.getDict(seriesnumber).keys():
                    summa = len(req.getDict(seriesnumber).keys())
                    a.query("UPDATE Episodes set %s = -1 where eid = %d;" %(elem.lower().replace(' ', ''), eid))
                    a.query('Update Episodes set original = 0 where eid = %d;' %eid)
                    a.query('Update Episodes set summ = %d' %summa)
                    a.save()

    comingseries = a.fetch('Select sname from Episodes where original = 0 group by sname')
    for i in comingseries: #series
        series = i[0].encode('utf-8')
        new = req.compare(series)
        print(new)
        for tr in new: #translations
            sid = bdserials.hashf(series)
            fetchepisodes = a.fetch("Select ename, eid from Episodes where %s = -1 order by date limit %d;" % (tr[0], tr[1]))
            for st in fetchepisodes:
                a.query('Update Episodes set %s = 0 where eid = %d;' %(tr[0].lower().replace(' ', ''), st[1]))
                a.save()
                summ = a.fetch('Select summ from Episodes where eid = %d;' %st[1])[0][0]
                summ -= 1
                if summ == 0:
                    a.query("Delete from Episodes where eid = %d;" %st[1])
                    a.save()
                else:
                    a.query("Update Episodes set summ = %d where eid = %d;" %(summ, st[1]))
                    a.save()
                fetchusers = a.fetch("Select uid from Podpiski where sid = %d and translation = \'%s\';" % (sid, tr[0]))
                for user in fetchusers:  # users
                    chat_id = user[0]
                    episode = st[0].encode('utf-8')
                    trans = tr[0].encode('utf-8')
                    token = '308210124:AAHkb6qVLTqo0pIKsn_IQTZqvYJ7wpzVJn0'
                    text = "Сегодня (%s) вы можете посмотреть серию \'%s\' сериала \'%s\' в озвучке \'%s\'" % (da1, episode, series, trans)
                    requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s' % (token, chat_id, text))
                    # sum = 0
                    # for j in req.getDict(series).keys():
                    #     sum = sum + int(a.fetch("Select %s from Episodes where eid = %d" %(j.lower().replace(' ', ''), st[1]))[0][0])
                    # if sum == 0:
                    #     a.query('Delete from Episodes where eid = %d' %(st[1]))



lastserial = ''
lasttranslation = ''
newseries = ''
newtranslation = ''

@post("/")
def subscribe():
    chat_id = request.json['message']['chat']['id']
    mess = request.json['message']['text']

    seriesid = bdserials.hashf(mess)
    lengthseries = len(a.fetch('SELECT sname from Serials where sid = %d;' % (seriesid)))
    print("main, mess:", mess, lengthseries, chat_id, "line 49")
    if lengthseries > 0:
        global lastserial
        lastserial = mess
        mess = '###seriesname'
    if mess == "Original" or mess == "Subs" or mess == "NewStudio" or mess == "LostFilm" or mess == "ColdFilm" or mess == "IdeaFilm" or mess == "LevshaFilm"  or mess == "Baibako"  or mess == "Fox" or mess == "":
        global lasttranslation
        lasttranslation = mess
        mess = '###translationname'

    st = StateTraveler(chat_id)
    curstate = st.getState()
    if curstate == 3 and mess.encode('utf-8') != "Назад":
        global newseries
        newseries = mess
        mess = '###anymessage'
    if curstate == 6 and mess.encode('utf-8') != "Назад":
        global newtranslation
        newtranslation = mess
        mess = '###anymessage'

    lastserial=lastserial.encode('utf-8')
    sid = bdserials.hashf(lastserial)
    lasttranslation = lasttranslation.encode('utf-8')
    print(mess, sid, lastserial, lasttranslation)
    res = st.handleMessage(mess, sid, lastserial, lasttranslation)
    if res != None:
        if res[0] == None: #no keyboard
            requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s' % (token, chat_id, res[1]))
        elif res[1] != None: #text
            requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s&reply_markup=%s' % (token, chat_id, res[1], res[0]))
        if res[2] != None: #action
            st.getFunction(res[2], lastserial, lasttranslation, newseries, newtranslation, token, res[0])

@get('/filedownload')
def stat_file():
    return static_file('serials.db', root=".", download=True)

run(host="0.0.0.0", port=os.environ.get('PORT', 5000))

