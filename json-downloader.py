import json
import time
from datetime import date
import configparser
from random import randint
from time import sleep
import requests
from urllib import parse

config = configparser.ConfigParser()
config.read("c:/bin/config.ini")
YOUR_ID = config.get("Configuration", "id")
YOUR_KEY = config.get("Configuration", "key")

dir = 'C:/Temp/Anonymous/'

today = date.today()

if today.day % 2 == 0:
    # Even
    phrases = open("anonymous-phrases-even.txt")
    print("It's an even day.")
else:
    # Odd
    phrases = open("anonymous-phrases-odd.txt")
    print("It's an odd day.")


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
    filename = dir + time.strftime("%Y%m%d-%H%M%S") + ".json"
    r = requests.get(search_url)
    f = open(filename, "w")
    json_str = json.dumps(r.json())
    f.write(json_str)
    f.close()


def pause_search():
    # Delay queries randomly to avoid being blocked
    print("Sleeping...")
    sleep(randint(10, 50))


for phrase in phrases:
    phrase = encode_phrase(phrase)
    url = get_url(phrase)
    pause_search()
    google_json = get_json(url)
