# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

class QSBK:

  def __init__(self):
    self.url = 'http://www.qiushibaike.com/hot/page/'
    self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    self.rex = '<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?>(.*?)</a>.*?<div.*?class="content".*?>(.*?)</div>(.*?)<div class="stats.*?class="number">(.*?)</i>'
    self.headers = {'User-Agent' : self.user_agent}
    self.stories = []
    self.enable = False
    self.page = 1

  def get_pages(self, page):
    url = self.url + str(page)
    try:
      request = urllib2.Request(url, headers = self.headers)
      response = urllib2.urlopen(request)
      # content = response.read()
      content = response.read().decode('utf-8')
      pattern = re.compile(self.rex, re.S)
      items = re.findall(pattern, content)
      return items
    except urllib2.URLError, e:
      if hasattr(e,"reason"):
        print u"连接糗事百科失败,错误原因"
        return None

  def load_page(self):
    items = self.get_pages(self.page)
    self.page += 1
    for item in items:
      # haveImg = re.search("img",item[2])
      # if not haveImg:
      self.stories.append([item[0].strip(),item[1].strip(),item[3].strip()])
    if len(self.stories) == 0:
      self.enable = False
      

  def start(self):
    print "正在读取糗事百科,按回车查看新段子，Q退出"
    self.enable = True
    self.load_page()

    while self.enable:
      input = raw_input()
      if input == "Q":
        self.enable = False
        continue

      if len(self.stories)>0:
        story = self.stories[0]
        del self.stories[0]
        print u"第%d页\t发布人:%s\n%s\n赞:%s\n" %(self.page - 1,story[0],story[1],story[2])
      
      if len(self.stories) == 0:
        self.load_page()
        

spider = QSBK()
spider.start()



      