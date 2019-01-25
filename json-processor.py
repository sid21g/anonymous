import os
import html
import configparser
from datetime import date
import re
from sqlite3 import connect
from sqlite3 import Error

config = configparser.ConfigParser()
config.read("c:/bin/config.ini")
YOUR_ID = config.get("Configuration", "id")
YOUR_KEY = config.get("Configuration", "key")

conn = connect(r"anon.db")
curs = conn.cursor()
today = date.today()

bold_tag = re.compile(r"<b>", re.MULTILINE)


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


dir_files = os.listdir(os.getcwd())
for file in dir_files:
    process_search_results(file)

# conn.close()
