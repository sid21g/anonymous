from flask import Flask, render_template, g
from sqlite3 import connect
from datetime import datetime
import re

app = Flask(__name__)
app.config.from_object(__name__)


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


extra_bold = re.compile("<\/b>.*?<b>", re.MULTILINE)


@app.template_filter('clean_content')
def clean_content(content):
    content = content.strip()
    content = content.replace('\n', ' ').replace('\r', '')
    content = content.replace('<b>...</b>', '...')
    content = content.replace('<br>', '')
    content = re.sub(extra_bold, "\1 ", content)
    return content


@app.template_filter('clean_title')
def clean_title(title):
    title = title.replace(' - WSJ', '')
    title = title.replace(' - Wsj.com', '')
    title = title.replace(' - The', '')
    title = title.replace(' | Reuters', '')
    title = title.replace('| Reuters', '')
    title = title.replace(' New York Times', '')
    title = title.replace(' - POLITICO', '')
    return title


@app.template_filter('name_source')
def name_source(source):
    if source == 'www.washingtonpost.com':
        return 'Washington Post'
    elif source == 'www.wsj.com':
        return 'Wall Street Journal'
    elif source == 'www.reuters.com':
        return 'Reuters'
    elif source == 'www.usatoday.com':
        return "USA Today"
    elif source == 'www.bloomberg.com':
        return "Bloomberg"
    elif source == 'www.nytimes.com':
        return "New York Times"
    elif source == 'hosted.ap.org':
        return "Associated Press"
    elif source == 'www.politico.com':
        return "Politico"
    else:
        return "Unknown source"


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
                       'DESC LIMIT 100')
    return render_template('index.html', entries=results)


@app.route('/date/<anon_date>')
def get_date(anon_date):
    results = query_db('SELECT '
                       'link, '
                       'source, '
                       'phrase, '
                       'title, '
                       'content, '
                       'date_entered '
                       'FROM '
                       'anon '
                       'WHERE '
                       'date_entered = ? '
                       'ORDER BY '
                       'date_entered '
                       'DESC LIMIT 100', anon_date)
    return render_template('date.html', entries=results)


@app.route('/outlet/<outlet_name>')
def fetch_outlet(outlet_name):
    results = query_db('SELECT '
                       'link, '
                       'source, '
                       'phrase, '
                       'title, '
                       'content, '
                       'date_entered '
                       'FROM '
                       'anon '
                       'WHERE '
                       'source = ? '
                       'ORDER BY '
                       'date_entered '
                       'DESC LIMIT 100', outlet_name)
    return render_template('outlet.html', entries=results)


if __name__ == '__main__':
    app.run(debug=True)
