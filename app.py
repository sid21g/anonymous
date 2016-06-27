from flask import Flask, render_template, g, current_app, request
from flask_paginate import Pagination
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
        "SELECT url FROM outlets WHERE name = ?",
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


@freezer.register_generator
def index():
    page, per_page, offset = get_page_items()
    print(page)
    page = '?page=' + str(page)
    yield {'index': page }


@app.route('/')
def index():
    total = query_db('select count(*) from anon', '', one=True)
    page, per_page, offset = get_page_items()
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
                       'anon.source = outlets.url '
                       'ORDER BY '
                       'date_entered DESC '
                       'LIMIT ?, ?', (offset, per_page))
    outlets = query_db("SELECT DISTINCT "
                       "outlets.name, "
                       "outlets.url "
                       "FROM outlets "
                       "JOIN anon "
                       "ON outlets.url = anon.source "
                       "ORDER BY outlets.name")
    pagination = get_pagination(page=page,
                                per_page=per_page,
                                total=next(iter(total.values())),
                                format_total=True,
                                format_number=True,
                                display_msg = '',
                                )
    return render_template('index.html',
                           entries=results,
                           page=page,
                           per_page=per_page,
                           outlets=outlets,
                           pagination=pagination)


@app.route('/outlet/<outlet_name>/')
def outlet(outlet_name):
    masthead = parse.unquote_plus(outlet_name)
    outlet_name_dict = fetch_outlet_url(outlet_name)
    outlet_url = outlet_name_dict['url']
    total = query_db('select count(*) from anon LEFT OUTER JOIN outlets ON anon.source = outlets.url WHERE anon.source = ?', (outlet_url,), one=True)
    page, per_page, offset = get_page_items()
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
                       "ON anon.source = outlets.url "
                       "WHERE anon.source = ? "
                       "ORDER BY anon.date_entered DESC "
                       "LIMIT ?, ?", (outlet_url, offset, per_page))
    outlets = query_db("SELECT DISTINCT "
                       "outlets.name, "
                       "outlets.url "
                       "FROM outlets "
                       "JOIN anon "
                       "ON outlets.url = anon.source "
                       "ORDER BY outlets.name")
    pagination = get_pagination(page=page,
                                per_page=per_page,
                                total=next(iter(total.values())),
                                format_total=True,
                                format_number=True,
                                display_msg='',
                                )
    return render_template('outlet.html',
                           entries=results,
                           page=page,
                           per_page=per_page,
                           masthead=masthead,
                           outlets=outlets,
                           pagination=pagination)


def get_css_framework():
    return current_app.config.get('CSS_FRAMEWORK', 'bootstrap3')


def get_link_size():
    return current_app.config.get('LINK_SIZE', 'sm')


def show_single_page_or_not():
    return current_app.config.get('SHOW_SINGLE_PAGE', False)


def get_page_items():
    page = int(request.args.get('page', 1))
    per_page = request.args.get('per_page')
    if not per_page:
        per_page = current_app.config.get('PER_PAGE', 20)
    else:
        per_page = int(per_page)

    offset = (page - 1) * per_page
    return page, per_page, offset


def get_pagination(**kwargs):
    kwargs.setdefault('record_name', 'records')
    return Pagination(css_framework=get_css_framework(),
                      link_size=get_link_size(),
                      show_single_page=show_single_page_or_not(),
                      **kwargs
                      )


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(debug=True)


