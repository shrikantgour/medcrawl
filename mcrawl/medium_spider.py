import scrapy
from scrapy.crawler import CrawlerProcess
import sqlite3
from datetime import date
from datetime import timedelta
con = sqlite3.connect('crawlt.db')
cur = con.cursor()
cur.execute('''DROP TABLE IF EXISTS pagedata''')
con.commit()
# Create table
cur.execute('''CREATE TABLE pagedata (No int, title text, readTime text, Day text, fullDate text,link text,fullpage text,tags text)''')
con.commit()
con.close()
# Insert a row of data
#cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")


class PostsSpider(scrapy.Spider):
    name = "posts"
    tag1 = "gaming"
    tag2 = "books"
    today = date.today()
    count = 0
    yesterday = today - timedelta(days = 1)
    d1 = yesterday.strftime("%Y/%m/%d")
    start_urls = [
        # "https://medium.com/tag/"+tag1+"/archive/"+str(d1),
        # "https://medium.com/tag/"+tag2+"/archive/"+str(d1)
        ]

    def parse(self,response):
        con = sqlite3.connect('crawlt.db')
        self.count = 1
        cur = con.cursor()

        page = response.url.split('/')[-1]
        filename = 'posts-%s.html' % page
        for i in range(1,30):
            title = (response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[2]/a/div/section/div[2]/div/h3/text()').get())
            readtime = (response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[1]/div/div/div[2]/div/span[2]/@title').get())
            time = (response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[1]/div/div/div[2]/div/a/time/text()').get())
            fulltime = (response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[1]/div/div/div[2]/div/a/time/@datetime').get())
            link = (response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[2]/a/@href').get())
            cur.execute("insert into pagedata(No,title,readTime,Day,fullDate,link) values (?, ?, ?, ?, ?, ?)", (i, title,readtime,time,fulltime,link))
            self.start_urls.append(link)
            print(self.start_urls)

            scrapy.Request(link,callback = self.parse2)
            # rsp = scrapy.Response(req.url)
            # rsp
            
            print('Post number:'+str(i))
            print(response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[2]/a/div/section/div[2]/div/h3/text()').get())
            print(response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[1]/div/div/div[2]/div/span[2]/@title').get())
            print(response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[1]/div/div/div[2]/div/a/time/text()').get())
            print(response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[1]/div/div/div[2]/div/a/time/@datetime').get())
            print(response.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div['+str(i)+']/div/div/div[2]/a/@href').get())

        
        print(self.count)
        # if(self.count (response.text,str1,response.url))
    # Save (commit) the changes
        con.commit()
        con.close()

    def parse2(self,response):
        print("in parse2")
        tags = response.xpath('//div/ul/li/a/text()').getall()
        str1 = "" 
        cur.execute("SELECT link FROM pagedata")
        rows = cur.fetchall()
             # traverse in the string  
             
        for ele in tags: 
            str1 += ele  
        query = "Update pagedata set fullpage = ? , tags = ? where link = ?"
        for row in rows:
            cur.execute(query,(response.text,str1,response.url))
            

process = CrawlerProcess()
tag1 = "books"

process.crawl(PostsSpider, start_urls=["https://medium.com/tag/"+tag1+"/archive/2021/02/02"])
# process.crawl(PostsSpider)

process.start()

#with open(filename,'wb') as f:
            
            
            #f.write('|||||||||||||')
            #/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div[2]/div/div/div[2]/a/div/section/div[2]/div/h3
            #/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div[1]/div/div/div[2]/a/@href -- ARTICLE LINK
            #/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div[2]/div/div/div[2]/a/div/section/div[2]/div/h3
                  #//*[@id="prerendered"]/div[3]/div/div/div[2]/div[2]/div[1]/div/div/div[2]/a/div/section/div[2]/div/h3/text() - article title
            #/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div[1]/div/div/div[2]/a/div/section/div[2]/div/h3/text() - article title
            #/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div[2]/div/div/div[2]/a/div/section/div[2]/div/h3/strong/text() - title before 2021
            #/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/span[2]/@title - time
            #path--------------------------------------------        -which article------
            #//*[@id="prerendered"]/div[3]/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/a
            #//*[@id="prerendered"]/div[3]/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/a/time/text - May 31
            #/html/body/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]/div[2]/div/div/div[1]/div/div/div[2]/div/a/time/text
            #//*[@id="prerendered"]/div[3]/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/a/time/@datetime - full date time
            #/html/body/div[1]/div[2]/div/div[3]/div/div/div[1]/div/ul/li[1]/a
            #/html/body/div[1]/div[2]/div/div[3]/div/div/div[1]/div/ul/li[2]/a
