import urllib.request
from xml.etree import ElementTree
from sqlite3 import connect
import re

conn = connect(r'C:\Temp\anon.db')
curs = conn.cursor()

# TODO: Create loop where will query all anonymous source phrases
# TODO: Remove namespaces from ElementTree find calls
url = 'https://goo.gl/lxR5Ib'
local_file, headers = urllib.request.urlretrieve(url, "C:/Temp/anonymous.txt")

tree = ElementTree.parse(local_file)
root = tree.getroot()
feed_title = root.find('{http://www.w3.org/2005/Atom}title')
pub_name = re.compile('.*new_york_times.*')
if re.match(pub_name, feed_title.text):
    source = 'New York Times'
source = ''
entries = root.findall('{http://www.w3.org/2005/Atom}entry')
for entry in entries:
    title = entry.find('{http://www.w3.org/2005/Atom}title')
    link = entry.find('{http://www.w3.org/2005/Atom}link')
    summary = entry.find('{http://www.w3.org/2005/Atom}summary')
    insert_values = [source, title.text, link.attrib['href'], summary.text]
    curs.execute("INSERT INTO anon VALUES (?, ?, ?, ?)", insert_values)
    conn.commit()
results = curs.execute("SELECT * FROM anon")

# TODO: Fix encoding error when printing in Visual Studio
# print(results.fetchall())
