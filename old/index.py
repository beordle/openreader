#coding:utf-8
import chardet,datetime,urllib,urlparse,urllib2,wsgiref.handlers,os,time
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from BSXPath import BSXPathEvaluator,XPathResult


class Chatper(db.Model):
    name = db.StringProperty()
    content = db.TextProperty(required=True)
    date = db.DateProperty()
    read_completed = db.BooleanProperty()


#大概的思路是用BR分割，每行如果不含<*>标签的话，那就起码一定是纯文字。而纯文字基本上就是正文了，冗余的部分就无所谓了。有很大的通用性。
def getcontent(html):
  html=html.replace('&nbsp;',' ')
  line=html.split('<br />')
  a=[]
  for n,i in zip(range(0,len(line)),line):
    if i.find('<')==-1:
      a.append(n)
  #    print i.replace('&nbsp;',' ')
  firstline=line[max(a[0]-1,0)]
  content=firstline[firstline.rfind('>')+1:]#.decode('utf-8')
  for i in a:
    content += line[i]#.decode('utf-8')
  lastline=line[a[len(a)-1]+1]
  content += lastline[:lastline.find('<')-1]#.decode('utf-8')
  return content 

def fetch(url):
  html=urllib.urlopen(url).read()
  return html

def getinfo(url,html):
  document = BSXPathEvaluator(html)
  setting={}
  setting['next_xpath']=u"//a[contains(text(),'下章') or contains(text(),'下一章') or contains(text(),'下一页') or contains(text(),'下页')]"
  setting['title_xpath']="//title"
  next_link = document.getFirstItem(setting['next_xpath'])['href']#获取下一页URL
  next_url=urlparse.urljoin(url,next_link)#修正为绝对URL
  title= document.getFirstItem(setting['title_xpath']).string
  #site=root=urlparse.urlparse(url).netloc
  return title,next_url


class Handler(webapp.RequestHandler):
  def get(self,method):
    int_time=time.time()
    if Chatper.all().count()==0:
      url='http://www.xiucaiwu.com/html/21/21118/4599479.html'
    while time.time()-int_time<5:
      html=urllib2.urlopen(url).read().decode('gbk')
      title,next_url=getinfo(url,html)
      content=getcontent(html)
      Chatper(content=content).put()
      url=next_url

    print ""
    for i in Chatper.all():
      print i.content

def main():
  application = webapp.WSGIApplication([('(.*?)', Handler)])
  wsgiref.handlers.CGIHandler().run(application)
if __name__ == '__main__':
  main()
