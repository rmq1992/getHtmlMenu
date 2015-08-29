import MySQLdb
import http.client, urllib.parse
from html.parser import HTMLParser

class MyHtmlParser(HTMLParser):
    litag = 0
    tdtag = 0
    atag = 0
    data = ''
    tagclass = ''
    end = 0
    def handle_starttag(self, tag, attrs):
        if(tag == 'ul'):
            self.litag = 1
        if(tag == 'table'):
            self.tdtag = 1
        if(tag == 'a'):
            if(self.tdtag == 1 or self.litag == 1):
                self.atag = 1
                for attr in attrs:
                    if attr[0] == "href":
                        self.data = attr[1]
                    elif attr[0] == "class":
                        if self.tagclass == '':
                            self.tagclass = attr[1]
                        elif self.tagclass != attr[1]:
                            self.atag = 0
                
    def handle_endtag(self, tag):
        if(tag == 'ul'):
            self.litag = 0
            self.end = 1
        if(tag == 'table'):
            self.tdtag = 0
            self.end = 1
        if(tag == 'a'):
            self.atag = 0
    
    def handle_data(self, data):
        if(self.atag == 1 and self.end == 0):
            print(self.data,':', data)
##            self.data = data

##parser = MyHtmlParser()
##url = '61.133.211.178'
##conn = http.client.HTTPConnection(url)
##try:
##    conn.request("GET","/")
##except TimeoutError as e:
##    print('timeout')
##else:
##    r1 = conn.getresponse()
##    if(r1.status == 200):
##        print(url)
##    response = r1.read()
##parser.feed(response.decode())
##result = parser.data

db = MySQLdb.connect(user='root', passwd='050954', db='dbapp_domains')
c = db.cursor()
count = c.execute("SELECT `key` FROM domains LIMIT 100")
urls = []
for data in c.fetchall():
    url = data[0]
    conn = http.client.HTTPConnection(url)
    try:
        conn.request("GET","/")
    except TimeoutError as e:
        print('timeout')
    except BaseException:
        pass
    else:
        r1 = conn.getresponse()
        if(r1.status == 200):
            urls.append(url)
##            response = r1.read()
##            if(response.count(b'location') == 0):
##                urls.append(url)
##                print('dns', url)
##    parser.feed(response.decode())
##    result = parser.data

##    print(r1.read())
