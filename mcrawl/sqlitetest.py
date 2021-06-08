
import sqlite3

con = sqlite3.connect('crawlt.db')
cur = con.cursor()
for row in cur.execute('SELECT No,title,readTime,Day,fullDate,link,tags FROM pagedata'):
    print(row)
    print('-------------------------------------------------------------------------------------------------------')
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
con.close()