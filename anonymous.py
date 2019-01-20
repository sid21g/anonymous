from urllib import parse
from urllib import request
from xml.etree import ElementTree
from sqlite3 import connect
from sqlite3 import Error
import configparser
from datetime import date
import re
from dupes import deletedupes
from csvwriter import writecsvfile
from fulltext import getfulltext

config = configparser.ConfigParser()
config.read("c:/bin/config.ini")
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
    restrict = "&dateRestrict=w1"
    exact = "&" + query
    language = "&hl=en"
    google_key = YOUR_KEY
    alt = "&alt=json"
    url = (base +
           query +
           google_id +
           restrict +
           exact +
           language +
           google_key +
           alt)
    anon_file = "anonymous.txt"
    # Delay queries randomly to avoid being blocked
    sleep(randint(10, 100))
    anon_file = "anonymous.json"
    local_file, headers = request.urlretrieve(url, anon_file)
    tree = ElementTree.parse(local_file)
    root = tree.getroot()
    entries = root.findall('{http://www.w3.org/2005/Atom}entry')

    # with open('C:/OneDrive/Projects/Code/Anonymous3/cse-json-response.json', encoding='utf8') as f:
    #     json_string = json.load(f)

    try:
        item_count = json_string["queries"]["request"][0]["count"]
    except Exception:
        item_count = 0
=======
    for entry in entries:
        title = entry.find('{http://www.w3.org/2005/Atom}title')
        link = entry.find('{http://www.w3.org/2005/Atom}link')
        source = link.attrib['title']
        summary = entry.find('{http://www.w3.org/2005/Atom}summary')
        insert_values = [source,

    for i in range(item_count):
        try:
            item_title = json_string["items"][i]["title"]
            item_link = json_string["items"][i]["link"]
            item_snippet = html.unescape(json_string["items"][i]["htmlSnippet"])
            item_source = json_string["items"][i]["displayLink"]
        except Exception:
            continue
        # Not all items have keywords
        try:
            item_keywords = json_string["items"][i]["pagemap"]["metatags"][0]["news_keywords"]
        except Exception:
            item_keywords = ''

        insert_values = [item_source,
                         phrase.strip(),
                         title.text,
                         link.attrib['href'],
                         summary.text,
                         item_title,
                         item_link,
                         item_snippet,
                         today]
        match = re.search(
            bold_tag,
            summary.text)  # Skip entries with no phrase in summary
        if match:
            try:
                curs.execute("INSERT INTO anon VALUES (?, ?, ?, ?, ?, ?)",
                             insert_values)
                conn.commit()
                print("New entry")
            except Error as e:
                print("Oops: ", e.args[0])
        else:
            print("No phrase in entry")

conn.close()
>>>>>>> parent of 947560a... Switch to JSON from discontinued Atom.

deletedupes()

writecsvfile()

getfulltext()
        try:
            curs.execute("INSERT INTO anon VALUES (?, ?, ?, ?, ?, ?)",
                         insert_values)
            conn.commit()
            print("New entry")
        except Error as e:
            print("Oops: ", e.args[0])
