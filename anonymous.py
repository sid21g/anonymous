import json
import html
from urllib import parse
from urllib import request
import configparser
from datetime import date
import re
from sqlite3 import connect
from sqlite3 import Error
from random import randint
from time import sleep

config = configparser.ConfigParser()
config.read("c:/Bin/config.ini")
YOUR_ID = config.get("Configuration", "id")
YOUR_KEY = config.get("Configuration", "key")

conn = connect(r"anon.db")
curs = conn.cursor()
today = date.today()
# We split phrase file in two to stay under 100 a day free limit
if today.day % 2 == 0:
    # Even
    phrases = open("anonymous-phrases-even.txt")
else:
    # Odd
    phrases = open("anonymous-phrases-odd.txt")
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
    # Delay queries randomly to avoid being blocked
    sleep(randint(10, 100))
    anon_file = "anonymous.json"
    local_file, headers = request.urlretrieve(url, anon_file)
    with open(local_file, encoding='utf8') as f:
        json_string = json.load(f)

    # with open('C:/OneDrive/Projects/Code/Anonymous3/cse-json-response.json', encoding='utf8') as f:
    #     json_string = json.load(f)

    try:
        item_count = json_string["queries"]["request"][0]["count"]
    except Exception:
        item_count = 0

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
                         item_title,
                         item_link,
                         item_snippet,
                         today]
        try:
            curs.execute("INSERT INTO anon VALUES (?, ?, ?, ?, ?, ?)",
                         insert_values)
            conn.commit()
            print("New entry")
        except Error as e:
            print("Oops: ", e.args[0])
