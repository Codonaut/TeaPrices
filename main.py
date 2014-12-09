'''
1) Unit Tests
2) Can I use app.config instead of settings?  Config with env variable
'''
from flask import Flask, render_template, g
import sqlite3
import settings
import requests
app = Flask(__name__)

'''
Next Up:
1) Get a database up and running
2) Think of how to represent data
    -- Need mapping of symbol to human readable name e.g.(THB to Thai Baht)
    -- Need mapping of symbol to price relative to dollar

3) 
'''

def connect_db():
    """Connects to the specific database."""
    return sqlite3.connect(settings.DATABASE)

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db

@app.teardown_request
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        g.db.close()

@app.before_request
def before_request():
    g.db = get_db()

@app.route("/")
def main():
    return render_template("line_chart.html")

@app.route("/_ingest_exchange_rates")
def ingest_exchange_rates():
    return ''

@app.route("/_update_currency_names")
def update_currency_names():
    r = requests.get(settings.OPEN_EXCHANGE_CURRENCY_LIST_URL)
    if r.status_code != 200:
        abort(500)
    results = r.json()
    queries = []
    for curr_code, curr_name in results.iteritems():
        queries.append('INSERT INTO currency_names (currency_name, currency_code) VALUES (%s, %s)' % (curr_name, curr_code))
    db_cursor = g.db.cursor()
    db_cursor.executemany(
        'INSERT INTO currency_names (currency_name, currency_code) VALUES (?, ?)', 
        [(name, code) for name, code in results.iteritems()]
    )
    g.db.commit()
    return ""

@app.route("/view_currencies")
def view_currencies():
    db_cursor = g.db.cursor()
    db_cursor.execute("SELECT * FROM currency_names")
    res = db_cursor.fetchall()
    return str(res)

if __name__ == "__main__":
    app.run(debug=settings.DEBUG)
