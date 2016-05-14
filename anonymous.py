import urllib.request
from xml.etree import ElementTree as ET

url = 'https://www.google.com/alerts/feeds/00081205862505704902/15214887296670213833'
local_file, headers = urllib.request.urlretrieve(url, "C:/Temp/anonymous.txt")

tree = ET.parse(local_file)
root = tree.getroot()
print(root)

