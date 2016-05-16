import urllib.request
from xml.etree import ElementTree
from sqlite3 import connect
import re

conn = connect(r'C:\Temp\anon.db')
curs = conn.cursor()

# TODO: Create loop where will query all anonymous source phrases
# TODO: Remove namespaces from ElementTree find calls
url = 'https://www.google.com/alerts/feeds/00081205862505704902/11030700134857925288'
local_file, headers = urllib.request.urlretrieve(url, "C:/Temp/anonymous.txt")

tree = ElementTree.parse(local_file)
root = tree.getroot()
title = root.find('{http://www.w3.org/2005/Atom}title')
pub_name = re.compile('.*new_york_times.*')
if re.match(pub_name, title.text):
    source = 'New York Times'
entries = root.findall('{http://www.w3.org/2005/Atom}entry')
for entry in entries:
   entry_title = entry.find('{http://www.w3.org/2005/Atom}title')
   entry_link = entry.find('{http://www.w3.org/2005/Atom}link')
   entry_content = entry.find('{http://www.w3.org/2005/Atom}content')
   insert_values = [source, entry_title.text, entry_link.attrib['href'], entry_content.text]
   curs.execute("INSERT INTO anon VALUES (?, ?, ?, ?)", insert_values)
   conn.commit()
results = curs.execute("SELECT * FROM anon")
#TODO: Fix encoding error when printing in Visual Studio
#print(results.fetchall())
