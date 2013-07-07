import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

from contextlib import closing

app = Flask(__name__)
app.config.from_object("config")

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.route('/')
def show_entries():
    cur = g.db.execute('select title, id from accounts')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('accounts.html', entries=entries)



if __name__ == "__main__":
    app.run()
