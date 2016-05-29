from urllib import parse
from urllib import request
from xml.etree import ElementTree
from sqlite3 import connect
from sqlite3 import Error
import configparser
from datetime import date
import re

config = configparser.ConfigParser()
config.read("config.txt")
YOUR_ID = config.get("Configuration", "id")
YOUR_KEY = config.get("Configuration", "key")

conn = connect(r"anon.db")
curs = conn.cursor()
phrases = open("anonymous-phrases.txt")
today = date.today()
bold_tag = re.compile(r"<b>", re.MULTILINE)

for phrase in phrases:
    query = phrase.strip()
    query = parse.quote_plus(query)

    base = 'https://www.googleapis.com/customsearch/v1?q='
    google_id = YOUR_ID
    restrict = "&dateRestrict=w2"
    exact = "&" + query
    language = "&hl=en"
    google_key = YOUR_KEY
    alt = "&alt=atom"
    url = (base+query+google_id+restrict+exact+language+google_key+alt)

    anon_file = "anonymous.txt"
    local_file, headers = request.urlretrieve(url, anon_file)
    tree = ElementTree.parse(local_file)
    root = tree.getroot()
    entries = root.findall('{http://www.w3.org/2005/Atom}entry')

    for entry in entries:
        title = entry.find('{http://www.w3.org/2005/Atom}title')
        link = entry.find('{http://www.w3.org/2005/Atom}link')
        source = link.attrib['title']
        summary = entry.find('{http://www.w3.org/2005/Atom}summary')
        insert_values = [source, phrase.strip(), title.text,
                         link.attrib['href'], summary.text, today]
        match = re.search(
            bold_tag, summary.text)  # Skip entries with no identifiable phrase
        if match:
            try:
                curs.execute("INSERT INTO anon VALUES (?, ?, ?, ?, ?, ?)",
                             insert_values)
                conn.commit()
            except Error as e:
                print("Oops: ", e.args[0])
        else:
            print("No phrase in entry")
