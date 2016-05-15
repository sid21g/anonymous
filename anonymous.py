import urllib.request
from xml.etree import ElementTree

url = 'https://www.google.com/alerts/feeds/00081205862505704902/15214887296670213833'
local_file, headers = urllib.request.urlretrieve(url, "C:/Temp/anonymous.txt")

tree = ElementTree.parse(local_file)
root = tree.getroot()

entries = root.findall('{http://www.w3.org/2005/Atom}entry')

for entry in entries:
   entry_title = entry.find('{http://www.w3.org/2005/Atom}title')
   entry_link = entry.find('{http://www.w3.org/2005/Atom}link')
   entry_content = entry.find('{http://www.w3.org/2005/Atom}content')
   print(entry_title.text)
   print(entry_link.attrib['href'])
   print(entry_content.text)
