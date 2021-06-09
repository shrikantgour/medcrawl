from os import sep
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
    start_urls =[]
    idcount = 1
    # rows = list(rows)
    # print(rows)
    # rows = rows.flatten()
    for row in rows:
        print ("Adding link : "+row[0])
        start_urls.append(row[0])
    con.close()
    pagenum = pgparam.objects.get(id = 1).num
    end = pagenum*10
    start = end-10
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
        print("TAGS**************************"+str1)
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
            # c.update(bgtag1 = tags[0],bgtag2 = tags[1],bgtag3 = tags[2],bgtag4 = tags[3],bgtag5 = tags[4])
        else:
            linkpat = response.request.meta['redirect_urls'][0]
            c = paged.objects.filter(bglink = linkpat)
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
        print("OOOOOOOOOOOOOOOOOOOOO")
        print(linkpat)
        link = response.url
        print(c)
        
        
    

process = CrawlerProcess()
process.crawl(PageSpider)
process.start()

 