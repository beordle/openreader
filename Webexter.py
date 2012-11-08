#coding: utf-8
import logging,sys
FORMAT = "%(asctime)-15s %(clientip)s %(user)-8s %(message)s"
logging.basicConfig(format=FORMAT,filename='text.log')
#    logging.basicConfig(filename='peng.log',level=loglevel)
#    if printtostdout:
#        soh = logging.StreamHandler(sys.stdout)
#logging.config.fileConfig('logging_basil.conf')
from BSXPath import BSXPathEvaluator,XPathResult
import urllib,urlparse,chardet
from ld import simiar
from config import config,yamlwrite
#大概的思路是用BR分割，每行如果不含<*>标签的话，那就起码一定是纯文字。而纯文字基本上就是正文了，冗余的部分就无所谓了。有很大的通用性。
def getcontent(html):
  html=html.replace('&nbsp;',' ')
  line=html.split('<br />')
  if len(line)<10:
    return None
  a=[]
  for n,i in zip(range(0,len(line)),line):
    if i.find('<')==-1:
      a.append(n)
  #    print i.replace('&nbsp;',' ')
  firstline=line[max(a[0]-1,0)]
  content=firstline[firstline.rfind('>')+1:]
  for i in a:
    content +='\r\n'+ line[i]+'\r\n'
  lastline=line[a[len(a)-1]+1]
  content += lastline[:lastline.find('<')-1]

  content=content
  #这个值很纠结，不知道了
  if len(content)<4:
    return None
  return content

def fetch(url):
  html=urllib.urlopen(url).read().decode('gbk')
  return html

def getinfo(url,html):
  document = BSXPathEvaluator(html)
  setting={}
  setting['next_xpath']=u"//a[contains(text(),'下章') or contains(text(),'下一章') or contains(text(),'下一页') or contains(text(),'下页') or contains(text(),'下一节')]"
  setting['title_xpath']="//title"
  title= ''+document.getFirstItem(setting['title_xpath']).string
  next_link = document.getItemList(setting['next_xpath'])
  if len(next_link)==0:
    return title,None
    pass
  next_url=urlparse.urljoin(url,next_link[0]['href'])#修正为绝对URL
  #site=root=urlparse.urlparse(url).netloc
  return title,next_url


#  print chardet.detect(next_url),type(next_url)
#  print chardet.detect(content),type(content)
#  print chardet.detect(title),type(title)
def getall(url):
  html=fetch(url)
  title,next_url=getinfo(url,html)
  content=getcontent(html)
  return title,content,next_url

def addchapter(book,bookname,title,content):
  import time
  if book.has_key(bookname):
    #进行存在性判断
    for i in book[bookname]:
      _CreatTime,_Title,_Content=i
      #差异度小于20%
      s=simiar(content,_Content)
      #过于相似为同章节
      if s<0.1:
         return book
  else:
    book[bookname]=[]
  chapter=[time.time(),title,content]
  #不存在则初始化
  book[bookname].append(chapter)
  return book
import random
def run(bookname,url):
  book={}
  while True:
    logging.info(url)
    title,content,next_url=getall(url)
    print next_url
    #如果一切正常，把它标记为正常页面
    if content!=None and next_url!=None:
      normal_url=url

    #如果下一页为空使用最近的正常页面,如果不是空的话继续下一页
    if next_url==None:
      url=normal_url
    else:
      url=next_url

    #这个页面可能是目录,主要为了防止目录中出现"下一章"
    if next_url.find('index')>0:
      url=normal_url
    if content!=None:
      book=addchapter(book,bookname,title,content)
      for _CreatTime,_Title,_Content in book[bookname]:
         file=open('a.txt','a')
         file.write(_Content.encode('gbk'))
         print _Title
    if url==normal_url:
      config[bookname]=[url]
      yamlwrite(config)
      return
for bookname in config.keys():
  for url in config[bookname]:
    run(bookname,url)