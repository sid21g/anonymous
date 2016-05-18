import urllib.request
from xml.etree import ElementTree
from sqlite3 import connect

conn = connect(r'C:\Temp\anon.db')
curs = conn.cursor()

# TODO: Remove namespaces from ElementTree find calls?

phrases = open("C:/Temp/anonymous-phrases.txt")
for phrase in phrases:

    query = phrase.strip()
    base = 'https://www.googleapis.com/customsearch/v1?q='
    query = query
    id = "&cx=012091639844104041986:munhfapni70&"
    restrict = "&dateRestrict=w2"
    exact = "&" + query
    language = "&hl=en"
    key = "&key=AIzaSyA6N7CSdYpxd2V5yYrVk316XiV46ec5Cqg"
    alt = "&alt=atom"
    url = (base + query + id + restrict + exact + language + key + alt)

    file = "C:/Temp/anonymous.txt"
    local_file, headers = urllib.request.urlretrieve(url, file)
    tree = ElementTree.parse(local_file)
    root = tree.getroot()
    feed_title = root.find('{http://www.w3.org/2005/Atom}title')
    entries = root.findall('{http://www.w3.org/2005/Atom}entry')

    for entry in entries:
        title = entry.find('{http://www.w3.org/2005/Atom}title')
        link = entry.find('{http://www.w3.org/2005/Atom}link')
        summary = entry.find('{http://www.w3.org/2005/Atom}summary')
        source = link.attrib['title']
        insert_values = [source, title.text, link.attrib['href'], summary.text]
        curs.execute("INSERT INTO anon VALUES (?, ?, ?, ?)", insert_values)
    conn.commit()
