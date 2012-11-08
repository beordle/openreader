#coding: utf-8
from BSXPath import BSXPathEvaluator,XPathResult
import urllib,urlparse,chardet
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


url='http://www.xiucaiwu.com/html/21/21118/4599479.html'
html=urllib.urlopen(url).read()
document = BSXPathEvaluator(html)
site=root=urlparse.urlparse(url).netloc

#XPath默认配置
setting={}
setting['next_xpath']="//a[contains(text(),'下章') or contains(text(),'下一章') or contains(text(),'下一页') or contains(text(),'下页')]"
setting['title_xpath']="//title"
#setting['context_xpath']="//*[id('content') or id('chapter_content')]"

#重新Load XPath设置
#修饰器
#获取下一页URL
next_link = document.getFirstItem(unicode(setting['next_xpath'],'utf-8'))['href']
next_url=urlparse.urljoin(url,next_link)
#context= str(document.getFirstItem(unicode(setting['context_xpath'],'utf-8'))).decode('utf-8')
content=getcontent(html)
title= document.getFirstItem(unicode(setting['title_xpath'],'utf-8')).string

print next_url,title,content
