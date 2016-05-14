import urllib.request
from xml.etree import ElementTree

url = 'https://www.google.com/alerts/feeds/00081205862505704902/15214887296670213833'
local_file, headers = urllib.request.urlretrieve(url, "C:/Temp/anonymous.txt")

# ElementTree.register_namespace('')
tree = ElementTree.parse(local_file)
root = tree.getroot()

entries = root.findall('{http://www.w3.org/2005/Atom}entry')

for entry in entries:
    print(entry.getchildren())

# print(list(root))

# Shows all child tags and attributes
# for child in root:
# 	print(child.tag)
