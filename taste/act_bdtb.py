# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import time

class BDTB:

  def __init__(self, target_url, see_lz):
    self.target_url = target_url
    self.see_lz = str(see_lz)
    self.file = None
    self.floor = 1

  def get_page(self, page):
    url = self.target_url + '?see_lz=' + self.see_lz + '&pn=' + str(page)
    try:
      request = urllib2.Request(url)
      response = urllib2.urlopen(request)
      # content = response.read().decode('utf-8')
      content = response.read()
      return content
    except urllib2.URLError, e:
      if hasattr(e,"reason"):
        print u"连接百度贴吧失败,错误原因"
        return None

  def get_title(self, page_content):
    pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
    result = re.search(pattern, page_content)
    if result:
      return result.group(1)
    else:
      return None

  def get_page_count(self, page_content):
    pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>.*?<span.*?>(.*?)</span>',re.S)
    result = re.search(pattern, page_content)
    if result:
      return result.group(2)
    else:
      return None

  def get_content(self, page_content):
    pattern = re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
    items = re.findall(pattern, page_content)
    content = []
    for item in items:
      #将文本进行去除标签处理，同时在前后加入换行符
      content = "\n"+item+"\n"
      contents.append(content.encode('utf-8'))
    return content

  def set_file(self, title):
    if title is not None:
      self.file = open(title + ".txt","w+")
    else:
      self.file = open(str(time.time()) + ".txt","w+")

  def write_data(self, contents):
    for item in contents:
      floorLine = "\n" + str(self.floor) + u"-----------------------------------------------------------------------------------------\n"
      self.file.write(floorLine)
      self.file.write(item)
      self.floor += 1

  def start(self):
    page_content = self.get_page(1)
    page_num = self.get_page_count(page_content)
    page_title = self.get_title(page_content)
    self.set_file(page_title)
    if page_num == None:
      print "URL已失效，请重试"
      return
    try:
      print "该帖子共有" + str(page_num) + "页"
      for i in range(1,int(page_num)+1):
        print "正在写入第" + str(i) + "页数据"
        page = self.get_page(i)
        contents = self.get_content(page)
        self.write_data(contents)
    except IOError,e:
      print "写入异常，原因" + e.message
    finally:
      print "写入任务完成"


print u"请输入帖子代号"
target_url = 'http://tieba.baidu.com/p/' + str(raw_input(u'ex: 2986369435\n'))
# seeLZ = raw_input("是否只获取楼主发言，是输入1，否输入0\n")
# floorTag = raw_input("是否写入楼层信息，是输入1，否输入0\n")
see_lz = 1

bdtb = BDTB(target_url, see_lz)
bdtb.start()