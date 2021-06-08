from os import sep
import scrapy
from scrapy.crawler import CrawlerProcess

import sqlite3

class PageSpider(scrapy.Spider):
    name = "pages"
    con = sqlite3.connect('crawlt.db')
    cur = con.cursor()
    cur.execute("SELECT link FROM pagedata")
    rows = cur.fetchall()
    start_urls =[]
    # rows = list(rows)
    # print(rows)
    # rows = rows.flatten()
    for row in rows:
        print (row[0])
        start_urls.append(row[0])
    con.close()
    print(start_urls)
    def parse(self,response):
        con = sqlite3.connect('crawlt.db')
        cur = con.cursor()
        tags = response.xpath('//div/ul/li/a/text()').getall()
        str1 = "" 
        for ele in tags: 
            str1 += ele
            str1+= ","
        print(str1)
        query = "Update pagedata set fullpage = ? , tags = ? where link = ?"
        cur.execute(query,(response.text,str1,response.url))
        
    # Save (commit) the changes
        con.commit()
        con.close()

process = CrawlerProcess()
# con = sqlite3.connect('crawlt.db')
# cur = con.cursor()
# cur.execute("SELECT link FROM pagedata")
# rows = cur.fetchall()
# for row in rows:
#     print(row[:-1])
#     process.crawl(PageSpider, start_urls=[row[:-1]])
process.crawl(PageSpider)
process.start()

 