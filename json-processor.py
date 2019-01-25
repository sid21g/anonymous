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
config.read("c:/bin/config.ini")
YOUR_ID = config.get("Configuration", "id")
YOUR_KEY = config.get("Configuration", "key")

conn = connect(r"anon.db")
curs = conn.cursor()

today = date.today()

# We split the phrase file in two to stay under 100 a day free limit
if today.day % 2 == 0:
    # Even
    phrases = open("anonymous-phrases-even.txt")
    print("It's an even day.")
else:
    # Odd
    phrases = open("anonymous-phrases-odd.txt")
    print("It's an odd day.")

bold_tag = re.compile(r"<b>", re.MULTILINE)


def encode_phrase(unencoded_phrase):
    unencoded_phrase = unencoded_phrase.strip()
    encoded_phrase = parse.quote_plus(unencoded_phrase)
    print("Encoded phrase: " + encoded_phrase)
    return encoded_phrase


def get_url(query):
    base = 'https://www.googleapis.com/customsearch/v1?q='
    google_id = YOUR_ID
    restrict = "&dateRestrict=w1"
    exact = "&" + query
    language = "&hl=en"
    google_key = YOUR_KEY
    alt = "&alt=json"
    request_url = (base +
                   query +
                   google_id +
                   restrict +
                   exact +
                   language +
                   google_key +
                   alt)
    print("Request url: " + request_url)
    return request_url


def get_json(search_url):
    anon_file = "anonymous.json"
    local_file, headers = request.urlretrieve(search_url, anon_file)
    with open(local_file, encoding='utf8') as f:
        json_string = json.load(f)
    # TODO: Save every JSON file to disk here
    return json_string


def update_database(results_json):
    item_source = results_json[0]
    item_phrase = results_json[1]
    item_title = results_json[2]
    item_link = results_json[3]
    item_snippet = results_json[4]
    insert_values = [item_source,
                     item_phrase,
                     item_title,
                     item_link,
                     item_snippet,
                     today]
    match = re.search(
        bold_tag,
        item_snippet)  # Skip entries with no phrase in summary
    if match:
        try:
            curs.execute("INSERT INTO anon VALUES (?, ?, ?, ?, ?, ?)",
                         insert_values)
            conn.commit()
            print("New entry inserted in the database.")
        except Error as e:
            print("Oops: ", e.args[0])
    else:
        print("Skipping. No anonymous phrase in the entry.")


def process_search_results(results_json, item_phrase):
    try:
        item_count = results_json["queries"]["request"][0]["count"]
    except Exception:
        print("This query did not return an item count.")
        item_count = 0
    for i in range(item_count):
        try:
            item_source = results_json["items"][i]["displayLink"]
            item_title = results_json["items"][i]["title"]
            item_link = results_json["items"][i]["link"]
            item_snippet = html.unescape(results_json["items"][i]["htmlSnippet"])
        except Exception:
            continue
        db_fields = [item_source, item_phrase, item_title, item_link, item_snippet]
        update_database(db_fields)


def pause_search():
    # Delay queries randomly to avoid being blocked
    print("Sleeping...")
    sleep(randint(10, 100))


for phrase in phrases:
    phrase = encode_phrase(phrase)
    url = get_url(phrase)
    pause_search()
    google_json = get_json(url)
    process_search_results(google_json, phrase)


conn.close()
