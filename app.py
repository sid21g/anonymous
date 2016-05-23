from flask import Flask, render_template
from sqlite3 import connect

app = Flask(__name__)
app.config.from_object(__name__)


def clean_content(content):
    content = content.strip()
    content = content.replace('<b>...</b>', '...')
    content = content.replace('<br>', '')
    content = content.replace('\n', ' ').replace('\r', '')
    return content


def clean_title(title):
    title = title.replace(' - WSJ', '')
    title = title.replace(' - Wsj.com', '')
    title = title.replace(' - The', '')
    title = title.replace(' | Reuters', '')
    return title


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
def index(name="John Doe"):
    conn = connect('anon.db')
    curs = conn.cursor()
    results = curs.execute('SELECT link, source, phrase, title, content, date_entered FROM anon ORDER BY date_entered DESC')
    entries = [dict(link=row[0], source=name_source(row[1]), phrase=row[2], title=clean_title(row[3]), content=clean_content(row[4]), date_entered=row[5]) for row in results.fetchall()]
    return render_template('index.html', name=name, entries=entries)
    conn.close()


@app.route('/outlet/<outlet>')
def outlet(outlet):
    return '<h1>Hello, %s!</h1>' % outlet


if __name__ == '__main__':
    app.run(debug=True)
