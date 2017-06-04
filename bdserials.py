import progfile
import classes
import hashlib
a = progfile.db()
# a.query("CREATE TABLE Serials(sid INTEGER NOT NULL PRIMARY KEY, sname TEXT NOT NULL, subs INTEGER, lostfilm INTEGER, newstudio INTEGER);")
# a.query("CREATE TABLE Episodes(eid INTEGER NOT NULL PRIMARY KEY autoincrement UNIQUE, sid INTEGER NOT NULL, senumber INTEGER NOT NULL, sname TEXT NOT NULL, enumber INTEGER NOT NULL, ename TEXT, date INTEGER NOT NULL);")
# a.query("CREATE TABLE Podpiski(pid INTEGER NOT NULL PRIMARY KEY autoincrement UNIQUE, sid INTEGER NOT NULL, uid INTEGER NOT NULL, status INTEGER, Podpiski TEXT);")
# a.query("CREATE TABLE Users(uid INTEGER NOT NULL, state INTEGER);")
# a.query("CREATE TABLE State(stateid INTEGER NOT NULL PRIMARY KEY autoincrement UNIQUE, fromState integer NOT NULL, toState integer NOT NULL, message text);")
# a.query("CREATE TABLE NewTranslations(ntid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, translation TEXT NOT NULL, series TEXT NOT NULL, user INTEGER NOT NULL)")
# a.query("CREATE TABLE NewSerials(nsid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, series TEXT NOT NULL, user INTEGER NOT NULL);")

def hashf(a):
    m = hashlib.md5()
    m.update(a.encode('utf-8'))
    e = m.hexdigest()
    b = int(e, 16)
    b=b//1000000000000000000000000
    return b

def addSerial(s):
    a.query('insert into Serials(sid, sname, subs, lostfilm, newstudio, original) values (\"%d\", \"%s\", 0, 0, 0, 0);' %(hashf(s.sname), s.sname))
    a.save()


def addEpisodes(s, e):
    a.query('insert into Episodes(sid, sname, senumber, enumber, ename, date) values (\'%d\', \'%s\', \'%d\', \'%d\', "%s", \'%s\');' %(hashf(s.sname), s.sname, e.senumber, e.enumber, e.ename, e.date))
    a.save()

def addPodpiski(sid, uid):
   a.query('insert into Podpiski(sid, uid) values (%d, %d);'%(sid, uid))
   a.save()

