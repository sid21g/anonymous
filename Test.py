import requests
from lxml import html

page = requests.get('http://nytimes.com')
tree = html.fromstring(page.content)

print(tree.text)


# soup = BeautifulSoup(doc, 'html.parser')

# print(soup.prettify())
