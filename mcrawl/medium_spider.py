import os
import sys
import django
import scrapy
from scrapy.crawler import CrawlerProcess
import sqlite3
from datetime import date
from datetime import timedelta
# from medcrawl import setup
# setup()
sys.path.append('../medcrawl/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'medcrawl.settings'
django.setup()
from mcrawl.models import paged,pgparam
con = sqlite3.connect('crawlt.db')
cur = con.cursor()
cur.execute('''DROP TABLE IF EXISTS pagedata''')
con.commit()
# Create table
cur.execute('''CREATE TABLE pagedata (No int, title text,author text, readTime text, Day text, fullDate text,link text,fullpage text,tags text)''')
con.commit()
con.close()

paged.objects.all().delete()

class PostsSpider(scrapy.Spider):
    name = "posts"
    tag1 = "gaming"
    tag2 = "books"
    
    count = 0
    today = date.today()
    yesterday = today - timedelta(days = 1)
    d1 = yesterday.strftime("%Y/%m/%d")
    start_urls = [
        # "https://medium.com/tag/"+tag1+"/archive/"+str(d1),
        # "https://medium.com/tag/"+tag2+"/archive/"+str(d1)
        ]
    print("IN MEDIUM SPIDER")
    def parse(self,response):
        con = sqlite3.connect('crawlt.db')
        self.count = 1
        cur = con.cursor()

        page = response.url.split('/')[-1]
        filename = 'posts-%s.html' % page

        related = (response.xpath('//div/div/ul/li/a/text()').getall())
        print("RELATED TAGS:"+str(related))
        a = pgparam.objects.latest('id')
        a.relatedtags = related
        a.save()
        pagenum = pgparam.objects.latest('id').num
        end = pagenum*10
        start = end-5
        print("START:"+str(start)+" END:"+str(end))
        for i in range(start,end):
            print("INSIDE FOR LOOP")
            title =    (response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[2]/a/div/section/div[2]/div/h3/text()').get())
            if title is None:
                print("null Title")
                end = end+1
                continue
            authorr = (response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[1]/div/div/div[2]/a[1]/text()').get())
            readtime = (response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[1]/div/div/div[2]/div/span[2]/@title').get())
            time =     (response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[1]/div/div/div[2]/div/a/time/text()').get())
            fulltime = (response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[1]/div/div/div[2]/div/a/time/@datetime').get())
            link =     (response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[2]/a/@href').get())
            
            substr = "?"
            link = link[:link.index(substr)]            
            cur.execute("insert into pagedata(No,title,author,readTime,Day,fullDate,link) values (?, ?, ?, ?, ?, ?, ?)", (i, title,authorr,readtime,time,fulltime,link))
            b = paged(pgno = i, bgtitle = title,bgauthor=authorr, bgread = readtime, bgdt = time, bgfdt = fulltime, bglink = link)
            b.save()
            
            self.start_urls.append(link)
            print(self.start_urls)

            # scrapy.Request(link,callback = self.parse2)
            print('Post number:'+str(i))
            print(response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[2]/a/div/section/div[2]/div/h3/text()').get())
            print(response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[1]/div/div/div[2]/a[1]/text()').get())
            print(response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[1]/div/div/div[2]/div/span[2]/@title').get())
            print(response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[1]/div/div/div[2]/div/a/time/text()').get())
            print(response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[1]/div/div/div[2]/div/a/time/@datetime').get())
            print(response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[2]/a/@href').get())

        
        print(self.count)
        # print(paged.objects.all)
        con.commit()
        con.close()
            

process = CrawlerProcess()
tag1 = pgparam.objects.latest('id').tag
#Model.objects.latest('field')
print("TAG IN MS:"+tag1)
today = date.today()
yesterday = today - timedelta(days = 1)
d1 = yesterday.strftime("%Y/%m/%d")
process.crawl(PostsSpider, start_urls=["https://medium.com/tag/"+tag1+"/archive/"+str(d1)])
process.start()
