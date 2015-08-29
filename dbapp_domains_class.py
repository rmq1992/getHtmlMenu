import MySQLdb
import http.client, urllib.parse
from html.parser import HTMLParser

count = 0

class CharsetHtmlParser(HTMLParser):
    charset = 'UTF-8'
    def handle_startendtag(self, tag, attrs):
        if(tag == 'meta'):
            for attr in attrs:
                if(attr[0] == 'content'):
                    contents = attr[1].split(';')
                    for content in contents:
                        if(content.count('charset') != 0):
                            self.charset = content.split('=')[1]

class MyHtmlParser(HTMLParser):
    menutag = 0
    atag = 0
    data = ''
    apair = []
    def handle_starttag(self, tag, attrs):
        if(tag == 'ul' or tag == 'ol' or tag == 'table'):
            self.menutag = 1
        elif(tag == 'a' and self.menutag == 1):
            self.atag = 1
            for attr in attrs:
                if attr[0] == "href":
                    self.data = attr[1]
                
    def handle_endtag(self, tag):
        if((tag == 'ul' or tag == 'ol' or tag == 'table') and self.menutag == 1 and len(self.apair) != 0):
            self.menutag = 0
            count += 1
            print(apair)
            self.apair.clear()
        elif(tag == 'a'):
            self.atag = 0
    
    def handle_data(self, data):
        if(self.atag == 1):
            if(len(self.apair) == 0 and data.count('首')+data.count('页') == 0):
                self.menutag = 0
            else:
                self.apair.append((self.data, data))
##            self.data = data

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

parser = MyHtmlParser()
charset_parser = CharsetHtmlParser()
with open('useful_url') as fp:
    url = fp.readline().replace('\n','')
    while(url):
        print(url)
        conn = http.client.HTTPConnection(url)
        conn.request("GET","/")
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        response = r1.read()
        charset_parser.feed(str(response))
        parser.feed(response.decode(charset_parser.charset))
        print(parser.apair)
        url = fp.readline().replace('\n','')

##    print(r1.read())
