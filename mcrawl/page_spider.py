import datetime
import os
import sys
import django
import scrapy
from scrapy.crawler import CrawlerProcess

import sqlite3
sys.path.append('../medcrawl/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'medcrawl.settings'
django.setup()
from mcrawl.models import paged,pgparam

class PageSpider(scrapy.Spider):
    name = "pages"
    print("IN PAGE SPIDER")
    print("PRINTING ALL DATA")
    print(paged.objects.all())
    con = sqlite3.connect('crawlt.db')
    cur = con.cursor()
    cur.execute("SELECT link FROM pagedata")
    rows = cur.fetchall()
    allpages = paged.objects.all()
    start_urls =[]
    if allpages:
        for page in allpages:
            if not page.bgtag1:
                start_urls.append(page.bglink)

    idcount = 1
    secstaken = 0.00
    con.close()
    print(start_urls)
    def parse(self,response):
        con = sqlite3.connect('crawlt.db')
        cur = con.cursor()
        #/html/body/div/div/div[3]/div[3]/div/div[1]/div/div[4]/ul/li[1]/a
        # /html/body/div[1]/div/div[3]/article/div/section[1]/div/div/div[2]/div/div/div[1]/div[2]/span/span/div/a/text() --author
        #/html/body/div[1]/div/div[3]/article/div/section[2]/div/div/ul/li[3]/a
        #/html/body/div[1]/div/div[3]/div[5]/div/div[1]/div/div[3]/ul/li[5]/a
        tags = response.xpath('//div/div/div/div/ul/li/a/text()').getall()
        postauthor = response.xpath('/html/body/div[1]/div/div[3]/article/div/section[1]/div/div/div[2]/div/div/div[1]/div[2]/span/span/div/a/text()').get()
        str1 = "" 
        for ele in tags: 
            str1 += ele
            str1+= ","
        str1 = str1[:-1]
        print("TAGS**"+str1)
        print(response.url)
        self.idcount = self.idcount+1
        linkpattern = '%'+response.url+'%'
        linkpat = response.url
        linkpat = linkpat.lstrip()
        linkpat = linkpat.rstrip()
        query = "Update pagedata set fullpage = ? , tags = ? where link = ?"
        cur.execute(query,(response.text,str1,linkpat))
        # Save (commit) the changes
        con.commit()
        con.close()
        c = paged.objects.filter(bglink = linkpat)
        if(c):
            print("NO REDIRECTS")
        else:
            linkpat = response.request.meta['redirect_urls'][0]
            c = paged.objects.filter(bglink = linkpat)
        pagetitle = response.xpath('//div/div/div/article/div/section/div/div/div/h1/text()').get()
        # athname = 
        authorname = c.get().bgauthor
        authorname= authorname.replace(" ","")
        
        filename = authorname+str(c.get().id)+".html"
        path = "./static/"+authorname+str(c.get().id)+".html"
        c.update(bgpage = path[1:])
        with open(path,'wb') as f:
            f.write(response.body)
        try:
            c.update(bgtag1 = tags[0])
        except:
            print("0 TAGS")
        try:
            c.update(bgtag2 = tags[1])
        except:
            print("1 TAGS")
        try:
            c.update(bgtag3 = tags[2])
        except:
            print("2 TAGS")
        try:
            c.update(bgtag4 = tags[3])
        except:
            print("2 TAGS")
        try:
            c.update(bgtag1 = tags[4])
        except:
            print("4 TAGS")
        print("LinkPattern")
        print(linkpat)
        link = response.url
        print(c)
        print("PAGE SPIDER STATS")
        secstaken = (datetime.datetime.utcnow() - self.crawler.stats.get_value('start_time')).total_seconds()
        print(secstaken)
        pg = pgparam.objects.latest('id')
        secstaken = (secstaken + pg.scrapetime)/(self.crawler.stats.get_stats()['response_received_count']+1)
        pg.scrapetime = secstaken
        pg.save()
        print(self.crawler.stats.get_stats())
        
process = CrawlerProcess()
process.crawl(PageSpider)
process.start()

 