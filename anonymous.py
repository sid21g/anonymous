# import urllib.request
# import json

# url = 'https://www.googleapis.com/customsearch/v1?q=who+declined+to+be+identified&cx=012091639844104041986:munhfapni70&dateRestrict=y1&exactTerms=who+declined+to+be+identified&key=AIzaSyA6N7CSdYpxd2V5yYrVk316XiV46ec5Cqg'
# response = urllib.request.urlopen(url)
# content = response.read()
# data = json.loads(content.decode('utf8'))

# # Count of matches returned. Apparently the max is 10.
# count = data['queries']['request'][0]['count']
# count = int(count)
# for i in range(count):
# 	print(data['items'][i]['title'])
# 	print(data['items'][i]['link'])
# 	print(data['items'][i]['displayLink'])
# 	print(data['items'][i]['htmlSnippet'])

import urllib.request
from xml.etree import ElementTree as ET
url = 'https://www.google.com/alerts/feeds/00081205862505704902/15214887296670213833'
response = urllib.request.urlopen(url)
content = response.read()

tree = ET.parse(content)
root = tree.getroot()
print(root)
