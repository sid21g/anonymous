import newspaper
from datetime import date
from sqlite3 import connect
from sqlite3 import Error


def getfulltext():

    anon_conn = connect('C:/Dropbox/Anonymous/anon.db')
    anon_curs = anon_conn.cursor()

    today = date.today()
    str_today = today.strftime('%Y-%m-%d')

    anon_curs.execute("SELECT source, link FROM anon WHERE date_entered = ?", (str_today,))
    # anon_curs.execute('SELECT source, link FROM anon LIMIT 5')

    for row in anon_curs.fetchall():
        source = row[0]
        link = row[1]
        a = newspaper.Article(link)
        a.download()
        a.parse()
        insert_values = [source,
                         link,
                         a.text,
                         today]
        full_conn = connect('C:/Dropbox/Anonymous/fulltext.db')
        full_curs = full_conn.cursor()
        try:
            full_curs.execute("INSERT INTO fulltext VALUES(?, ?, ?, ?)", insert_values)
            full_conn.commit()
            print("The full text has been inserted")
        except Error as e:
            print("Oops: ", e.args[0])
        full_conn.close()

    anon_conn.close()

