class Serials:
    sid = None
    sname = ""

    def __init__(self, sname):
        self.sname = sname


class Episodes:
    sid = ""
    senumber = ""
    enumber = ""
    ename = ""
    date = ""

    def __init__(self, sid, senumber, enumber, ename, date):
        self.sid = sid
        self.senumber = senumber
        self.enumber = enumber
        self.ename = ename
        self.date = date


class Podpiski:
    pid = ""
    sid = ""
    uid = ""

    def __init__(self, pid, sid, uid):
        self.pid = pid
        self.sid = sid
        self.uid = uid
