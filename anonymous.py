import urllib.request
from xml.etree import ElementTree
from sqlite3 import connect
import configparser

# TODO: Remove namespaces from ElementTree find calls?
# TODO: Handle when reach free query limit

config = configparser.ConfigParser()
config.read("config.txt")

YOUR_ID = config.get("Configuration", "id")
YOUR_KEY = config.get("Configuration", "key")

conn = connect(r'C:/Temp/anon.db')
curs = conn.cursor()

phrases = open("C:/Temp/anonymous-phrases.txt")
for phrase in phrases:

    query = phrase.strip()
    base = 'https://www.googleapis.com/customsearch/v1?q='
    query = query
    id = YOUR_ID
    restrict = "&dateRestrict=w2"
    exact = "&" + query
    language = "&hl=en"
    key = YOUR_KEY
    alt = "&alt=atom"
    url = (base + query + id + restrict + exact + language + key + alt)
    print(url)

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
