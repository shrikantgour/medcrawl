import datetime
import os
import sys
import django
import scrapy
from scrapy.crawler import CrawlerProcess
import sqlite3
import scrapy.statscollectors
from datetime import date,timedelta
sys.path.append('../medcrawl/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'medcrawl.settings'
django.setup()
from mcrawl.models import paged,pgparam
con = sqlite3.connect('crawlt.db')
cur = con.cursor()
cur.execute('''DROP TABLE IF EXISTS pagedata''')
print("DELETED SQLITE TABLE")
con.commit()
# Create table
cur.execute('''CREATE TABLE pagedata (No int, title text,author text, readTime text, Day text, fullDate text,link text,fullpage text,tags text)''')
con.commit()
con.close()
previoustag = pgparam.objects.latest('id').prevtag
currenttag = pgparam.objects.latest('id').tag
looper = pgparam.objects.latest('id').loopcount
print("PREVIOUS TAG: "+previoustag+" CURRENTTAG: "+currenttag)
if previoustag != currenttag and previoustag!="" and looper==1:
    paged.objects.all().delete()
    print("DELETED Django PAGED")
   
class PostsSpider(scrapy.Spider):
    name = "posts"
    count = 0
    today = date.today()
    td1 = today.strftime("%d")
    yesterday = today - timedelta(days = pgparam.objects.latest('id').subfromtoday)
    d1 = yesterday.strftime("%Y/%m/%d")
    start_urls = []
    secstaken = 0.00
    print("IN MEDIUM SPIDER")
    def parse(self,response):
        print(response.status)
        con = sqlite3.connect('crawlt.db')
        self.count = 1
        cur = con.cursor()
        nullcount = 0
        dupcount = 0
        page = response.url.split('/')[-1]
        filename = 'posts-%s.html' % page

        related = (response.xpath('//div/div/ul/li/a/text()').getall())
        print("RELATED TAGS:"+str(related))
        if not related:
            print("NO RELATED TAGS FOUND!")
        a = pgparam.objects.latest('id')
        a.relatedtags = related
        a.save()
        pg =  pgparam.objects.latest('id')
        if(pg.remainingarticles):
            end = pg.endnum - (10 - pg.remainingarticles)
            print("HAS REMAINING ARTICLES:"+ str(pg.remainingarticles))
        else:
            end = pg.endnum
            print("NO REMAINING ARTICLES")
        start = pg.startnum
        print("START:"+str(start)+" END:"+str(end))
        for i in range(start,end):
            print("INSIDE FOR LOOP")
            title = (response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[2]/a/div/section/div[2]/div/h3/text()').get())
            if title is None:
                title = (response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[2]/a/div/section/div[2]/div/h3/strong/text()').get())
            if title is None:
                print("null Title")
                if(nullcount<1):
                    end = end+1
                    nullcount= nullcount+1
                    continue
                print("after null title")
                remaining = end-i
                pg.remainingarticles = remaining
                pg.subfromtoday = pg.subfromtoday + 1
                
                numm = 1
                endat = numm*10 +1
                startfrom = endat-10
                pg.num = numm
                pg.startnum = startfrom
                pg.endnum = endat
                pg.errcode = 96
                pg.save()
                print("REMAINING ARTICLES: "+str(pg.remainingarticles)+" SUB FROM TODAY: "+str(pg.subfromtoday))
                break
            nullcount=0
            alreadyexist = paged.objects.filter(bgtitle__icontains = title)
            if not alreadyexist:
                print("ALREADYEXIST NULL")
                if paged.objects.all():
                    print("PREVIOUSTITLE IN IF "+str(paged.objects.latest('id').bgtitle))
                    if str(title) == str(paged.objects.latest('id').bgtitle):
                        print("FOUND BG Title"+ title)
                        alreadyexist = 1
                        dupcount = dupcount+1
                    else:
                        dupcount = 0
            print("PRINTING ALRDYEXST:"+str(alreadyexist))
            if paged.objects.all():
                    print("PREVIOUS TITLE :"+str(paged.objects.latest('id').bgtitle))
            if alreadyexist:
                dupcount = dupcount+1
            else:
                dupcount = 0
            if (alreadyexist and dupcount >1) or len(alreadyexist)>1 :
                print("DUPLICATE Title"+ title)
                remaining = end-i
                pg.remainingarticles = remaining
                today = date.today()
                td1 = today.strftime("%d")
                pg.subfromtoday = pg.subfromtoday + int(td1)
                numm = 1
                endat = numm*10 +1
                startfrom = endat-10
                pg.num = numm
                pg.startnum = startfrom
                pg.endnum = endat
                pg.errcode = 96
                pg.save()
                print("Remaining: "+str(remaining)+" sub from today: "+td1+" num: "+str(numm)+" startfrom: "+str(startfrom)+" end at: "+str(endat))
                break
            authorr = (response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[1]/div/div/div[2]/a[1]/text()').get())
            readtime = (response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[1]/div/div/div[2]/div/span[2]/@title').get())
            time =     (response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[1]/div/div/div[2]/div/a/time/text()').get())
            fulltime = (response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[1]/div/div/div[2]/div/a/time/@datetime').get())
            link =     (response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[2]/a/@href').get())
            
            substr = "?"
            link = link[:link.index(substr)]            
            print("SAVING IN SQLITE")
            cur.execute("insert into pagedata(No,title,author,readTime,Day,fullDate,link) values (?, ?, ?, ?, ?, ?, ?)", (i, title,authorr,readtime,time,fulltime,link))
            pagenum = None
            if paged.objects.all():
                pagenum = int(paged.objects.latest('id').pgno)
                pagenum = pagenum+1
            if not pagenum:
                pagenum = i
            print("SAVING IN DJANGO")
            b = paged(pgno = pagenum, bgtitle = title,bgauthor=authorr, bgread = readtime, bgdt = time, bgfdt = fulltime, bglink = link)
            b.save()
            
            # self.start_urls.append(link)
            # print(self.start_urls)

            # scrapy.Request(link,callback = self.parse2)
            print('Post number:'+str(i))
            print(response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[2]/a/div/section/div[2]/div/h3/text()').get())
            print(response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[1]/div/div/div[2]/a[1]/text()').get())
            print(response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[1]/div/div/div[2]/div/span[2]/@title').get())
            print(response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[1]/div/div/div[2]/div/a/time/text()').get())
            print(response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[1]/div/div/div[2]/div/a/time/@datetime').get())
            print(response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[2]/a/@href').get())
            print("i:"+str(i)+" end:"+str(end))
            if str(i) == str(end-1):
                pg.remainingarticles = 0
                pg.errcode = 200
                pg.save()
            else:
                pg.errcode = 100
        print("MEDIUM SPIDER STATS")
        secstaken =(datetime.datetime.utcnow() - self.crawler.stats.get_value('start_time')).total_seconds()
        print(secstaken)
        pg.scrapetime = secstaken
        pg.save()
        print(self.count)
        # print(paged.objects.all)
        con.commit()
        con.close()
            

process = CrawlerProcess()
tag1 = pgparam.objects.latest('id').tag
#Model.objects.latest('field')
print("TAG IN MS:"+tag1)
today = date.today()
yesterday = today - timedelta(days = pgparam.objects.latest('id').subfromtoday)
d1 = yesterday.strftime("%Y/%m/%d")
urltoscrape = "https://medium.com/tag/"+tag1+"/archive/"+str(d1)
print("SCRAPING URL - " + urltoscrape)
process.crawl(PostsSpider, start_urls=[urltoscrape])
process.start()
