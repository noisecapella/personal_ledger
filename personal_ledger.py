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
def index():
    return redirect(url_for('accounts'))

@app.route('/accounts')
def accounts():
    cur = g.db.execute('SELECT accounts.full_title, SUM(withdrawal), SUM(deposit) FROM accounts LEFT OUTER JOIN transactions ON transactions.account_id = accounts.id GROUP BY accounts.id ORDER BY accounts.full_title')
    accounts = [dict(title=row[0], withdrawal=row[1] or 0.0, deposit=row[2] or 0.0) for row in cur.fetchall()]
    return render_template('accounts.html', accounts=accounts)

@app.route('/add_account', methods=['POST', 'GET'])
def add_account():
    if request.method == 'POST':
        flash("TODO: submit account info")
        return redirect(url_for('accounts'))
    return render_template('add_account.html')


if __name__ == "__main__":
    app.run()
