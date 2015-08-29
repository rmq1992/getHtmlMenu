import MySQLdb
import http.client, urllib.parse
from html.parser import HTMLParser

class MyHtmlParser(HTMLParser):
    menutag = 0
    atag = 0
    script_tag = 0
    end = 0
    data = ''
    apair = []
    charset = 'UTF-8'
##    set charset, default is utf-8
    def deal_meta_tag(self, attrs):
        for attr in attrs:
            if(attr[0] == 'content'):
                contents = attr[1].split(';')
                for content in contents:
                    if(content.count('charset') != 0):
                        self.charset = content.split('=')[1]
    def handle_startendtag(self, tag, attrs):
        if(tag == 'meta'):
            self.deal_meta_tag(attrs)
    def handle_starttag(self, tag, attrs):
        if(tag == 'script'):
            self.script_tag = 1
        elif(tag == 'meta'):
            self.deal_meta_tag(attrs)
        elif(tag == 'ul' or tag == 'ol' or tag == 'table'):
            self.menutag = 1
        elif(tag == 'a' and self.menutag == 1):
            self.atag = 1
            for attr in attrs:
                if attr[0] == "href":
                    self.data = attr[1]
                
    def handle_endtag(self, tag):
        if(tag == 'script'):
            self.script_tag = 0
        elif((tag == 'ul' or tag == 'ol' or tag == 'table') and self.menutag == 1 and len(self.apair) != 0):
            self.menutag = 0
            self.end += 1
            print(self.apair)
            self.apair.clear()
        elif(tag == 'a'):
            self.atag = 0
    
    def handle_data(self, data):
        if(self.atag == 1):
            if(len(self.apair) == 0 and (data.count('首') + data.count('页') < 2)):
                self.menutag = 0
            elif(self.data != ''):
                self.apair.append((self.data, data))
                self.data = ''
##            self.data = data
        elif(self.script_tag == 1):
            if(data.count('search.114so.cn') != 0):
                print('114')
                self.end = 1

##parser = MyHtmlParser()
##url = 'www.chinadbstar.com.cn'
##conn = http.client.HTTPConnection(url)
##conn.request("GET","/")
##r1 = conn.getresponse()
##print(r1.status, r1.reason)
##response = r1.read()
##parser.feed(response.decode())
##result = parser.data

##db = MySQLdb.connect(user='root', passwd='050954', db='dbapp_domains')
##c = db.cursor()
##count = c.execute("SELECT `key` FROM domains ORDER BY IP LIMIT 10,20")
                
##for data in c.fetchall():
##    url = data[0]
##    print(url)

url = 'stzx.nxnet.cn'
##parser = MyHtmlParser()
##conn = http.client.HTTPConnection(url)
##conn.request("GET","/")
##r1 = conn.getresponse()
##print(r1.status, r1.reason)
##
##for line in r1:
##    try:
##        parser.feed(line.decode(parser.charset))
##    except UnicodeDecodeError as ude:
##        print(ude)
##    if(parser.end == 1):
##        break

with open('useful_url') as fp:
    parser = MyHtmlParser()
    for url in fp:
        parser.end = 0
        url = url.replace('\n','')
        conn = http.client.HTTPConnection(url)
        conn.request("GET","/")
        r1 = conn.getresponse()
        print(url, r1.status, r1.reason)
        for line in r1:
            try:
                parser.feed(line.decode(parser.charset))
            except UnicodeDecodeError as ude:
                print(ude)
            if(parser.end == 1):
                break
##        conn = http.client.HTTPConnection(url)
##        conn.request("GET","/")
##        r1 = conn.getresponse()
##        print(r1.status, r1.reason)
##        response = r1.read()
##        charset_parser.feed(str(response))
##        parser.feed(response.decode(charset_parser.charset))
##        print(parser.apair)

##    print(r1.read())
