# # -*- coding: utf-8 -*-
# # for run
# import os
# import json
# import requests
# import progfile
# import bdserials
# from datetime import datetime, date
# from bottle import run, request, get, post, static_file
#
#
# a = progfile.db()
#
#
# b = a.fetch('select sname from Serials')
# dic = {"keyboard": b}
# keyboard = json.dumps(dic)
#
#
# sspisok = ''
# for i in range(len(b)):
#     c = str(b[i])
#     c = c[2:-3]
#     sspisok = sspisok+'\n'+c
#
#
# @get("/notify")
# def notify():
# #    da1 = date(2017, 3, 20)
#     da = datetime.today()
#     da1 = datetime.date(da)
#     da = int(datetime.toordinal(da1))
#     sendinfo=a.fetch('SELECT Podpiski.uid, Episodes.sname, Episodes.ename from Episodes inner join Podpiski on Podpiski.sid = Episodes.sid where (Episodes.date+Podpiski.status) = %d;' %da)
#     token = '308210124:AAHkb6qVLTqo0pIKsn_IQTZqvYJ7wpzVJn0'
#     for i in sendinfo:
#         text = "Today (%s) you can watch \'%s\' of \'%s\'. Have a good day!" %(da1, i[2], i[1])
#         chat_id = i[0]
#         requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s' % (token, chat_id, text))
#
#
# @post("/")
# def ListOfSerials():
#     token = '308210124:AAHkb6qVLTqo0pIKsn_IQTZqvYJ7wpzVJn0'
#     chat_id = request.json['message']['chat']['id']
#     tetext = request.json['message']['text']  # text which user wrote
#     #tetext = str(tetext)
#     if tetext.find('"') != -1:
#         textik = tetext[tetext.find('"') + 1: tetext.rfind('"')] # text between "" (name of serial, if user printed something from keyboardchoose)
#     else:
#         textik = ""
#     textikid = bdserials.hashf(textik)  # hash(text between "")
#     lengthtextik = len(a.fetch('SELECT sname from Serials where sid = %d;' % (textikid)))  # if we have serial called
#     if tetext == "/start":  # if we just started
#         text = "Hello, sunshine! You can choose a series:"
#         requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s&reply_markup=%s' % (token, chat_id, text, keyboard))
#     elif tetext == "No, I don't want to unsubscribe":
#         text = "Sunshine! You can choose a new series."
#         requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s&reply_markup=%s' % (token, chat_id, text, keyboard))
#     elif tetext[:tetext.find('"')]=='Yes, I want to unsubscribe from ': #don't delete the PROBEL
#         sid = bdserials.hashf(tetext[(tetext.find('"')+1):-1])
#         a.query('Delete from Podpiski where (uid = %d and sid = %d);' %(chat_id, sid))
#         a.save()
#         text = "You have unsubscribed successfully from \"%s\"!" %(tetext[(tetext.find('"')+1):-1])
#         requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s&reply_markup=%s' % (token, chat_id, text, keyboard))
#     elif lengthtextik > 0:  # if we have serial called text between ""
#         st = tetext[tetext.rfind('"') + 2:]  # type of translation (if user printed something from keyboardchoose)
#         if st == "original" or st == "subs" or st == "newstudio" or st == "lostfilm":
#             if st == "original":
#                 a.query('UPDATE Podpiski SET status = 0 WHERE(uid = %d and sid = %d);' %(chat_id, textikid))
#                 a.save()
#             else:
#                 p = (a.fetch('SELECT %s from serials where sid = %d;' %(st, textikid)))
#                 a.query('UPDATE Podpiski SET status = %d WHERE(uid = %d and sid = %d);' % (p[0][0], chat_id, textikid)) #error: type
#                 a.save()
#             text = "You will receive a notification when you will be able to watch a new episode. You can choose more series."
#             requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s&reply_markup=%s' % (token, chat_id, text, keyboard))
#
#     else:
#         teid = bdserials.hashf(tetext)
#         length = len(a.fetch('SELECT sname from Serials where sid = %d;'%(teid)))
#         if length > 0:
#             statuss = a.fetch('Select status from Podpiski where uid = %d and sid = %d;' %(chat_id, teid))
#             if len(statuss) == 0:
#                 text = "You have subscribed successfully to \'%s\'! Please, choose if you want to get message when the original episode, russian subs, newstudio or lostfilm transtation appear." % (tetext)
#                 bdserials.addPodpiski(teid, chat_id)
#                 keyboardchoose = {"keyboard": [["\"%s\" original" %(str(tetext))], ["\"%s\" subs" %str(tetext)], ["\"%s\" newstudio" %str(tetext)], ["\"%s\" lostfilm" %str(tetext)]]}
#                 keyboardchoose = json.dumps(keyboardchoose)
#                 requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s&reply_markup=%s' % (token, chat_id, text, keyboardchoose))
#             else:
#                 text = "You have already subscribed on \"%s\". Do you want to unsubscribe?" % (tetext)
#                 keyboarddelete = {"keyboard": [["Yes, I want to unsubscribe from \"%s\"" %(tetext)], ["No, I don't want to unsubscribe"]]}
#                 keyboarddelete = json.dumps(keyboarddelete)
#                 requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s&reply_markup=%s' % (token, chat_id, text, keyboarddelete))
#         else:
#             text = "Sorry, we don't have that series :("
#             requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s' % (token, chat_id, text))
#
#
# @get('/filedownload')
# def stat_file():
#     return static_file('serials.db', root=".", download=True)
#
# run(host="0.0.0.0", port=os.environ.get('PORT', 5000))

