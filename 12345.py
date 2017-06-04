lastserial = ''
lasttranslation = ''
newseries = ''
newtranstalion =''


@post("/")
def subscribe():
    chat_id = request.json['message']['chat']['id']

    mess = request.json['message']['text']
    seriesid = bdserials.hashf(mess)  # hash(text between "")
    lengthseries = len(a.fetch('SELECT sname from Serials where sid = %d;' % (seriesid)))
    if lengthseries > 0:
        lastserial = mess
        if len(a.fetch('SELECT pid from Podpiski where uid = %d and sid = %d;' % (chat_id, seriesid)))!=0:
            mess = '###seriesname subscribed'
        else:
            mess = '###seriesname unsubscribed'
    if mess == "original" or mess == "subs" or mess == "newstudio" or mess == "lostfilm":
        lasttranslation = mess
        mess = '###translationname'

    st = StateTraveler(chat_id)
    curstate = st.getState()
    if curstate == 3:
        newseries = mess
        mess = '###anymessage'
    if curstate == 6:
        newtranstalion = mess
        mess = '###anymessage'

    res = st.handleMessage(mess)
    if res == None:
        send_message(chat_id, "Error")
    else:
        send_message_with_keyboard(chat_id, mess, st.getKeyboard())
