import urllib.request
import json

url = 'https://www.googleapis.com/customsearch/v1?q=who+declined+to+be+identified&cx=012091639844104041986:munhfapni70&dateRestrict=y1&exactTerms=who+declined+to+be+identified&key=AIzaSyA6N7CSdYpxd2V5yYrVk316XiV46ec5Cqg'
response = urllib.request.urlopen(url)
content = response.read()
data = json.loads(content.decode('utf8'))

count = data['queries']['request'][0]['count']
count = int(count)
for i in range(count):
	print(data['items'][i]['title'])

# print(count)
# Get the total number of results retured to collect examples
# results = data['searchInformation']['totalResults']
# print(results)

# for i in range(int(results)):
# 	print(data['items'][i]['title'])

# print(data)
# print(data['items'][0]['title']) # Works
# print(data['searchInformation']['totalResults'])
