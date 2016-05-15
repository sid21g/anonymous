import urllib.request
from xml.etree import ElementTree
from sqlite3 import connect

conn = connect(r'C:\Temp\anon.db')
curs = conn.cursor()

# TODO: Create loop where will query all anonymous source phrases
url = 'https://www.google.com/alerts/feeds/00081205862505704902/15214887296670213833'
local_file, headers = urllib.request.urlretrieve(url, "C:/Temp/anonymous.txt")

tree = ElementTree.parse(local_file)
root = tree.getroot()
entries = root.findall('{http://www.w3.org/2005/Atom}entry')
for entry in entries:
   entry_title = entry.find('{http://www.w3.org/2005/Atom}title')
   entry_link = entry.find('{http://www.w3.org/2005/Atom}link')
   entry_content = entry.find('{http://www.w3.org/2005/Atom}content')
   insert_values = [entry_title.text, entry_link.attrib['href'], entry_content.text]
   curs.execute("INSERT INTO anon VALUES (?, ?, ?)", insert_values)
   conn.commit()
results = curs.execute("SELECT * FROM anon")
print(results.fetchall())

