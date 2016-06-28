from flask import Flask, render_template, g
from sqlite3 import connect
from datetime import datetime
import re
from urllib import parse
from flask_frozen import Freezer
import sys
import configparser

config = configparser.ConfigParser()
config.read("config.txt")
FREEZER_DESTINATION = config.get("Configuration", "destination")

app = Flask(__name__)
app.config['FREEZER_DESTINATION'] = FREEZER_DESTINATION
app.config.from_object(__name__)
app.config['FREEZER_RELATIVE_URLS'] = True
freezer = Freezer(app)
extra_bold = re.compile(r"</b>.*?<b>", re.MULTILINE)


def connect_db():
    return connect("anon.db")


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def fetch_outlet_url(outlet_name):
    outlet_name = parse.unquote_plus(outlet_name)
    outlet_url = query_db(
        "SELECT source FROM outlets WHERE name = ?",
        (outlet_name,),
        one=True)
    return outlet_url


@app.template_filter('datetimeformat')
def datetimeformat(value, date_format='%B %e, %Y'):
    d = datetime.strptime(value, '%Y-%m-%d')
    return d.strftime(date_format)


@app.template_filter('clean_content')
def clean_content(content):
    content = content.strip()
    content = content.replace('\n', ' ').replace('\r', '')
    content = content.replace('<b>...</b>', '...')
    content = content.replace('<br>', '')
    content = re.sub(extra_bold, "\1 ", content)
    return content


# Makes for prettier URLs
@app.template_filter('plus_for_spaces')
def plus_for_spaces(content):
    content = content.strip()
    content = content.replace(' ', '+')
    return content


@app.route('/')
def index():
    results = query_db('SELECT anon.source, '
                       'outlets.name, '
                       'anon.phrase, '
                       'anon.title, '
                       'anon.link, '
                       'anon.content, '
                       'anon.date_entered '
                       'FROM '
                       'anon '
                       'LEFT OUTER JOIN '
                       'outlets '
                       'ON '
                       'anon.source = outlets.source '
                       'ORDER BY '
                       'date_entered DESC '
                       'LIMIT 250')
    outlets = query_db("SELECT DISTINCT "
                       "outlets.name, "
                       "outlets.source "
                       "FROM outlets "
                       "JOIN anon "
                       "ON outlets.source = anon.source "
                       "ORDER BY outlets.name")
    return render_template('index.html', entries=results, outlets=outlets)


@app.route('/outlet/<outlet_name>/')
def outlet(outlet_name):
    masthead = parse.unquote_plus(outlet_name)
    outlet_name_dict = fetch_outlet_url(outlet_name)
    outlet_url = outlet_name_dict['url']
    results = query_db("SELECT "
                       "anon.link, "
                       "outlets.name, "
                       "anon.source, "
                       "anon.phrase, "
                       "anon.title, "
                       "anon.content, "
                       "anon.date_entered "
                       "FROM "
                       "anon "
                       "LEFT OUTER JOIN outlets "
                       "ON anon.source = outlets.source "
                       "WHERE anon.source = ? "
                       "ORDER BY anon.date_entered DESC "
                       "LIMIT 250", (outlet_url,))
    outlets = query_db("SELECT DISTINCT "
                       "outlets.name, "
                       "outlets.source "
                       "FROM outlets "
                       "JOIN anon "
                       "ON outlets.source = anon.source "
                       "ORDER BY outlets.name")
    return render_template('outlet.html',
                           entries=results,
                           masthead=masthead,
                           outlets=outlets)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(debug=True)


