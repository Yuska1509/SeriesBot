# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import progfile
from bdserials import a

def getDict(seriesnumber):

    url = 'http://i9j1i7rmhp9.xyz/video/serials/pl/sound/%s/' %(seriesnumber)
    headers = {'Host' : 'i9j1i7rmhp9.xyz',
    'Upgrade-Insecure-Requests' :	'1',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Accept' :	'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer' :	'http://couber.be/video/serials/pl/sound/%s/' %(seriesnumber) ,
    'Accept-Encoding'	: 'gzip, deflate, sdch',
    'Accept-Language' :	'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'}

    r = requests.get(url, headers=headers)
    r = r.text
    soup = BeautifulSoup(r, "html5lib")
    soup = soup.findAll('script', {'type': 'text/javascript'})
    soup = soup[1].text[11:-3]
    soup = soup.split('],[')
    for i in range(1, len(soup)):
        soup[i] = len(soup[i].split(','))
    b = soup[1:]
    d={}
    soup[0] = soup[0].split(',')
    print(soup[0][2].encode('latin1').decode('utf8'))
    print(soup[0][1].encode('latin1').decode('utf8'))
    for i in range(len(soup[0])):
        # if soup[0][i][1:-1].isalnum():
        d2 = {soup[0][i][1:-1] : b[i]}
        d.update(d2)
    return d

#print(getDict('518'))     #bbt  -207, fargo - 518, homeland - 384, murder - 228, legion - 443, silicon valley - 524,

def updateNum(seriesname, translation, seriesnumber):
#    seriesnumber = a.fetch('Select num from Serials where sname = \'%s\'' %seriesname)[0][0]
    a.query('Update Serials set %s = %d where sname = \'%s\'' %(translation.lower(), getDict(seriesnumber).get(translation), seriesname))
    a.save()

def compare(seriesname):
    seriesnumber = a.fetch('Select num from Serials where sname = \'%s\'' % seriesname)
    if seriesnumber == None:
        return None
    seriesnumber = seriesnumber[0][0]
    for j in getDict(seriesnumber).keys():
        fetch = a.fetch('Select %s from Serials where sname = \'%s\'' % (j.lower(), seriesname))
        if fetch[0][0] != 0:
            if fetch[0][0] < getDict(seriesnumber).get(j):
                updateNum(seriesname, j, seriesnumber)
                return seriesname, j

serieslist = a.fetch('Select sname from Serials')
for elem in serieslist:
    series = elem[0]
    print(series)
    num = a.fetch("Select num from Serials where sname = \'%s\'" %series)
    print(num)
    if num != None:
        num = num[0][0]
        trlist = getDict(num).keys()
        print()
        for tr in trlist:
            updateNum(series, tr, num)
#print(compare('Legion'))
