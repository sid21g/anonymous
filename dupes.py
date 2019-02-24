from sqlite3 import connect
from sqlite3 import Error


conn = connect(r"/var/www/html/anonymous/anon.db")
curs = conn.cursor()

try:
    curs.execute('DELETE '
                 'FROM anon '
                 'WHERE ROWID '
                 'NOT IN '
                 '(SELECT min(ROWID) '
                 'FROM anon '
                 'GROUP BY source, content)')
    conn.commit()
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
    conn.commit()
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
    conn.commit()
    print("Cursor executed!")
except Error as e:
    print("Oops, duplicate link deletion didn't work: ", e.args[0])

SQL_statements = ["DELETE FROM anon WHERE link LIKE '%http://www.nytimes.com/by/%';",
                  "DELETE FROM anon WHERE link LIKE '%https://apnews.com/RogerStone%';",
                  "DELETE FROM anon WHERE link LIKE '%https://www.axios.com/authors/%';",
                  "DELETE FROM anon WHERE link LIKE '%https://www.cnn.com/videos/%';",
                  "DELETE FROM anon WHERE link LIKE '%https://www.nytimes.com/search%';",
                  "DELETE FROM anon WHERE link LIKE '%https://www.nytimes.com/reuters%';",
                  "DELETE FROM anon WHERE link LIKE '%https://www.nytimes.com/aponline%';",
                  "DELETE FROM anon WHERE link LIKE '%https://www.politico.com/morningeducation/%';",
                  "DELETE FROM anon WHERE link LIKE '%https://abcnews.go.com/WN%';",
                  "DELETE FROM anon WHERE link LIKE '%https://www.politico.com/morningtax/%';",
                  "DELETE FROM anon WHERE link LIKE '%https://www.politico.com/morningtech/%';",
                  "DELETE FROM anon WHERE link LIKE '%https://www.politico.com/newsletters%';",
                  "DELETE FROM anon WHERE link LIKE '%https://www.politico.com/states/new-york/newsletters%';",
                  "DELETE FROM anon WHERE link LIKE '%https://www.washingtonpost.com/people/%';",
                  "DELETE FROM anon WHERE link LIKE '%https://www.wsj.com/livecoverage/%';"]

for statement in SQL_statements:
    curs.execute(statement)
    conn.commit()
    print("Executed!")

conn.close()
