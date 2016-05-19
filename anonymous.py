import urllib.request
from xml.etree import ElementTree
import sqlite3
from sqlite3 import connect
import configparser

# TODO: Remove namespaces from ElementTree find calls?
# TODO: Handle when reach free query limit

config = configparser.ConfigParser()
config.read("config.txt")
YOUR_ID = config.get("Configuration", "id")
YOUR_KEY = config.get("Configuration", "key")

conn = connect(r'anon.db')
curs = conn.cursor()

phrases = open("anonymous-phrases-test.txt")

for phrase in phrases:

    query = phrase.strip()
    base = 'https://www.googleapis.com/customsearch/v1?q='
    id = YOUR_ID
    restrict = "&dateRestrict=w2"
    exact = "&" + query
    language = "&hl=en"
    key = YOUR_KEY
    alt = "&alt=atom"
    url = (base + query + id + restrict + exact + language + key + alt)

    # TODO: Clean up query phrase to remove quotes and + or urlencode?

    file = "anonymous.txt"
    local_file, headers = urllib.request.urlretrieve(url, file)
    tree = ElementTree.parse(local_file)
    root = tree.getroot()
    entries = root.findall('{http://www.w3.org/2005/Atom}entry')
    for entry in entries:
        title = entry.find('{http://www.w3.org/2005/Atom}title')
        link = entry.find('{http://www.w3.org/2005/Atom}link')
        source = link.attrib['title']
        summary = entry.find('{http://www.w3.org/2005/Atom}summary')
        insert_values = [source, phrase, title.text, link.attrib['href'], summary.text]
        # Handle inserts that violate unique constraint
        try:
            curs.execute("INSERT INTO anon VALUES (?, ?, ?, ?, ?)", insert_values)
            conn.commit()
        except sqlite3.IntegrityError:
            print("Dupe")
