# -*- coding: utf-8 -*-

import bdserials
import requests
from bdserials import a


def UnsubscribeFromSeries(seriesname, chat_id, token, keyboard):
    sid = bdserials.hashf(seriesname)
    a.query('Delete from Podpiski where (sid = %d and uid = %d);' %(sid, chat_id))
    a.save()
    seriesname = seriesname.encode("utf-8")
    text = "Вы отписались от сериала %s" %seriesname
    requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s&reply_markup=%s' % (token, chat_id, text, keyboard))

def NewSeries(newseries, chat_id, token, keyboard):
    newseries = newseries.replace('"', "'")
    a.query('Insert into NewSerials(series, user) values (\"%s\", \"%d\")' % (newseries, chat_id))
    a.save()
    text = "Спасибо за предложение! Мы постараемся учесть Ваше пожелание"
    requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s&reply_markup=%s' % (token, chat_id, text, keyboard))

def NewTranslation(newtranslation, series, chat_id, token, keyboard):
    text = "Спасибо за предложение! Мы постараемся учесть Ваше пожелание"
    newtranslation = newtranslation.replace('"', "'")
    requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s&reply_markup=%s' % (token, chat_id, text, keyboard))
    a.query('Insert into NewTranslations(translation, series, user) values (\"%s\", \"%s\", \"%d\")' % (newtranslation, series, chat_id))
    a.save()

def UnsubscibeFromTranslation(translation, series, chat_id, token, keyboard):
    sid = bdserials.hashf(series)
    a.query('Delete from Podpiski where (sid = %d and uid = %d and translation = \'%s\')' %(sid, chat_id, translation))
    a.save()
    series = series.encode("utf-8")
    translation = translation.encode("utf-8")
    text = "Вы отписались от сериала %s в озвучке %s" % (series, translation)
    requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s&reply_markup=%s' % (token, chat_id, text, keyboard))

def SubscribeToSeries(translation, series, chat_id, token, keyboard):
    sid = bdserials.hashf(series)
    a.query('Insert into Podpiski (sid, uid, translation) values (%d, %d, \'%s\')' % (sid, chat_id, translation))
    a.save()
    series = series.encode("utf-8")
    translation = translation.encode("utf-8")
    text = ("Вы подписались на сериал %s в озвучке %s" %(series, translation))
    requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s&reply_markup=%s' % (token, chat_id, text, keyboard))

def function6(chat_id, token, keyboard):
    text = "Список каких сериалов Вы хотите увидеть?"
    requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s&reply_markup=%s' % (token, chat_id, text, keyboard))

def function7(series, chat_id, token, keyboard):
    series = series.encode("utf-8")
    text = "Вы уже подписаны на сериал %s" %series
    requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s&reply_markup=%s' % (token, chat_id, text, keyboard))

def function8(series, chat_id, token, keyboard):
    text = "Сериал %s" %series
    requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s&reply_markup=%s' % (token, chat_id, text, keyboard))