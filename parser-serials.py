from bs4 import BeautifulSoup
import requests
import bdserials
import classes
from datetime import datetime, date

# url = "https://en.wikipedia.org/wiki/List_of_Homeland_episodes"
# url = "https://en.wikipedia.org/wiki/Stranger_Things#Season_2"
# url = "https://en.m.wikipedia.org/wiki/List_of_Silicon_Valley_episodes"                 #sname id: section_0  (19-20)
# url = "https://en.wikipedia.org/wiki/Legion_(TV_series)"                                #enumber scope: row   (45-46)
url = "https://en.wikipedia.org/wiki/List_of_Game_of_Thrones_episodes"                  #no new episodes
# url = "https://en.wikipedia.org/wiki/List_of_How_to_Get_Away_with_Murder_episodes"      #no new episodes
# url = "https://en.wikipedia.org/wiki/List_of_The_Big_Bang_Theory_episodes"              #no new episodes
# url = "https://en.wikipedia.org/wiki/List_of_Fargo_episodes"

html_doc = requests.get(url).text

soup = BeautifulSoup(html_doc, "html5lib")

#sn = soup.find('h1', {'id': 'section_0'})
sn = soup.find('h1', {'class': 'firstHeading'})
sname = sn.find('i').text
print(sname)

sid = bdserials.hashf(sname)

s = classes.Serials(sname)
bdserials.addSerial(s)

da = datetime.today()
da = datetime.date(da)
da0=str(da)
da1= int(da0[0:4]+da0[5:7]+da0[8:10])

tableseason = soup.findAll('table', {'class': 'wikitable plainrowheaders wikiepisodetable'})
senumber = 0
for i in tableseason:
    episode = i.findAll('tr', {'class': 'vevent'})
    senumber += 1
    for j in episode:
        dat = j.find('span', {'class': 'bday dtstart published updated'}).text
        date1 = int(dat[0:4]+dat[5:7]+dat[8:10])
        if date1<=da1:
           continue
        else:
            enumber = int(j.find('td').text)
#            enumber = int(j.find('th', {'scope': 'row'}).text)
            ename = j.find('td', {'class': 'summary'}).text
            ename = ename.replace('"', '')
            x = ename.find('[')
            y = ename.find(']')
            if x != -1:
                ename = ename[0: x] + ename[y+1:]
            print(senumber, enumber, ename)
        dat = date(int(dat[:4]), int(dat[5:7]), int(dat[8:]))
        dat = int(datetime.toordinal(dat))
        hv='insert into Episodes(sid, sname, senumber, enumber, ename, date) values (\'%d\', \'%s\', \'%d\', \'%d\', %s, \'%s\');'
        e = classes.Episodes(sid, senumber, enumber, ename, dat)
        print(hv % (bdserials.hashf(s.sname), s.sname, e.senumber, e.enumber, e.ename, e.date))
        bdserials.addEpisodes(s, e)