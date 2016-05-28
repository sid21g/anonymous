from flask import Flask, render_template, g, request
from sqlite3 import connect
from datetime import datetime
import re

app = Flask(__name__)
app.config.from_object(__name__)
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


@app.route('/')
def index():
    results = query_db('SELECT '
                       'link, '
                       'source, '
                       'phrase, '
                       'title, '
                       'content, '
                       'date_entered '
                       'FROM '
                       'anon '
                       'ORDER BY '
                       'date_entered '
                       'DESC LIMIT 500')
    return render_template('index.html', entries=results)


@app.route('/outlet/<outlet_name>', methods=['GET'])
def outlet(outlet_name):
    results = query_db("SELECT "
                       "link, "
                       "source, "
                       "phrase, "
                       "title, "
                       "content, "
                       "date_entered "
                       "FROM "
                       "anon "
                       "WHERE "
                       "anon.source = ? "
                       "ORDER BY "
                       "anon.date_entered "
                       "DESC LIMIT 100", (outlet_name,))
    return render_template('outlet.html', entries=results)


if __name__ == '__main__':
    app.run(debug=True)
