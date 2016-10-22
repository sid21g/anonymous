import newspaper
import sqlite3

conn = sqlite3.connect('C:/Temp/anon.db')
curs = conn.cursor()
curs.execute('SELECT link FROM anon LIMIT 5')

# TODO: Add code to insert text into database
for row in curs.fetchall():
    link = row[0]
    a = newspaper.Article(link)
    a.download()
    a.parse()
    print(a.text)

conn.close()


