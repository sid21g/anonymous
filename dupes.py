from sqlite3 import connect
from sqlite3 import Error


def deletedupes():

    conn = connect(r"anon.db")
    curs = conn.cursor()

    try:
        curs.execute('DELETE '
                     'FROM anon '
                     'WHERE ROWID '
                     'NOT IN '
                     '(SELECT min(ROWID) '
                     'FROM anon '
                     'GROUP BY source, content)')
        print("Cursor executed!")
    except Error as e:
        print("Oops, duplicate content deletion didn't work: ", e.args[0])
    try:
        curs.execute('DELETE '
                     'FROM anon '
                     'WHERE ROWID '
                     'NOT IN '
                     '(SELECT min(ROWID) '
                     'FROM anon '
                     'GROUP BY source, title)')
        print("Cursor executed!")
    except Error as e:
        print("Oops, duplicate title deletion didn't work: ", e.args[0])
    try:
        curs.execute('DELETE '
                     'FROM anon '
                     'WHERE ROWID '
                     'NOT IN '
                     '(SELECT min(ROWID) '
                     'FROM anon '
                     'GROUP BY source, link)')
        print("Cursor executed!")
    except Error as e:
        print("Oops, duplicate link deletion didn't work: ", e.args[0])

conn.close()