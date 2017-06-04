# -*- coding: utf-8 -*-
# for run
import json
import Functions
import req

from bdserials import a
#from progfile import db


class StateTraveler:
#    a = db()
    user_id = 0
    state = 0

    def __init__(self, user):
        self.user_id = user
        self.getState()

    def getState(self):
        res = a.fetch("SELECT state FROM Users WHERE uid = %d" % (self.user_id))
        if len(res) == 0:
            self.createUser()
            return self.state
        state = res[0][0]
        self.state = state
        return state

    def createUser(self):
        state = 0
        a.query("INSERT INTO Users (uid, state) VALUES (%d, %d);" % (self.user_id, state))
        a.save()

    def handleMessage(self, message, sid, series, translation):
        travelerreturn = self.travelState(message, sid, series, translation)
        print('trstate', travelerreturn)
        if travelerreturn[0] == None and message != "/start":
            return None
        keyboard = self.getKeyboard(series)
        return keyboard, travelerreturn[1], travelerreturn[2]


    def travelState(self, message, sid, series, translation):
        fetch = a.fetch("SELECT toState FROM State WHERE (message = \"%s\" and fromState = %d);" % (message, self.state))
        if len(fetch) == 0:
            return None, None
        tostate = fetch[0][0]
        Message = self.getMessage(tostate)
        if self.state == tostate == 1 and len(a.fetch('Select sid from Podpiski where uid = %d' %(self.user_id))) != 0:
            Message = "Сериалы, на которые Вы подписаны"
            tostate = 2
        if self.state == 4 and tostate == 1 and message == "###translationname" and len(a.fetch('Select pid from Podpiski where (sid = %d and uid = %d and translation = \'%s\');' %(sid, self.user_id, translation))) != 0:
            tostate = 5
            Message = "Вы уже подписаны на сериал %s в озвучке %s" %(series, translation)
        if self.state == 7 and tostate == 4 and len(a.fetch('Select pid from Podpiski where (sid = %d and uid = %d);' % (sid, self.user_id))) == 0:
            tostate = 8
            Message = "Выберите озвучку"
            print('3',Message, tostate)
        a.query("UPDATE Users Set state =%d where uid = %d;" % (tostate, self.user_id))
        a.save()
        action = a.fetch('Select action from State where (fromState = %d and toState = %d and message = \"%s\")' %(self.state, tostate, message))
        if len(action) != 0:
            action = action[0][0]
        self.state = tostate
        newstate = self.state
        return newstate, Message, action

    def getKeyboard(self, series):
        fetch = a.fetch("Select message, isWide from State where (fromState = %d and (isWide = -2 or isWide = -3 or isWide = -4));"% (self.state))
        buttonsArray = []
        i = 0
        while i < len(fetch):
            if fetch[i][1] == -2:
                buttonsArray = a.fetch('Select sname from Serials order by sname;')
                i += 1
            elif fetch[i][1] == -4:
                buttonsArray = a.fetch('Select Serials.sname from Serials inner join Podpiski on Serials.sid = Podpiski.sid where Podpiski.uid = %d group by sname order by sname;' %(self.user_id))
                i += 1
            elif fetch[i][1] == -3:
                # buttonsArray = [["Original"], ['Subs'], ['NewStudio'], ['LostFilm']]
                # i += 1
                num = a.fetch("Select num from Serials where sname = \'%s\';" %series)
                print("num:", len(num), num)
                if num[0][0] != None:
                    num = num[0][0]
                    for j in req.getDict(str(num)).keys():
                        buttonsArray.append([j.encode('utf-8')])
                buttonsArray.append(["Original"])
                buttonsArray.sort()
                i += 1
        fetch = a.fetch("Select message from State where (fromState = %d and isWide = 1);" % (self.state))
        i = 0
        while i < len(fetch):
            buttonsArray.append([fetch[i][0]])
            i += 1
        fetch = a.fetch("Select message from State where (fromState = %d and isWide = 0);"% (self.state))
        i = 0
        while i < len(fetch):
            if i + 1 != len(fetch):
                buttonsArray.append([fetch[i][0], fetch[i + 1][0]])
                i += 2
            else:
                buttonsArray.append([fetch[i][0]])
                i += 1
        return json.dumps({'keyboard': buttonsArray, 'resize_keyboard': True})

    def getMessage(self, tostate):
        fetch = a.fetch("SELECT message FROM State WHERE (isWide=4 and fromState = %d and toState = %d);" % (self.state,(tostate)))
        if len(fetch) != 0:
            mess = fetch[0][0]
            return mess
        return None


    def getFunction(self, action, series, translation, newseries, newtranslation, token, keyboard):
        if action == 1:
            Functions.UnsubscribeFromSeries(series, self.user_id, token, keyboard)
        if action == 2:
            Functions.NewSeries(newseries, self.user_id,token, keyboard)
        if action == 3:
            Functions.NewTranslation(newtranslation, series, self.user_id, token, keyboard)
        if action == 4:
            Functions.UnsubscibeFromTranslation(translation, series, self.user_id, token, keyboard)
        if action == 5:
            Functions.SubscribeToSeries(translation, series, self.user_id, token, keyboard)
        if action == 6:
            Functions.function6(self.user_id, token, keyboard)
        if action == 7:
            Functions.function7(series, self.user_id, token, keyboard)
        if action == 8:
            Functions.function8(series, self.user_id, token, keyboard)