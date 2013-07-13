import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import csv
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

@app.route('/transactions')
def transactions():
    cur = g.db.execute('SELECT transactions.description, withdrawal, deposit, accounts.full_title, other_transaction_id FROM transactions JOIN accounts ON transactions.account_id == accounts.id')
    transactions = [dict(description=row[0], withdrawal=row[1] or 0.0, deposit=row[2] or 0.0, account_name=row[3], other_transaction_id=row[4]) for row in cur.fetchall()]
    return render_template('transactions.html', transactions=transactions, title="Transactions")

@app.route('/accounts')
def accounts():
    cur = g.db.execute('SELECT accounts.full_title, SUM(withdrawal), SUM(deposit) FROM accounts LEFT OUTER JOIN transactions ON transactions.account_id = accounts.id GROUP BY accounts.id ORDER BY accounts.full_title')
    accounts = [dict(title=row[0], withdrawal=row[1] or 0.0, deposit=row[2] or 0.0) for row in cur.fetchall()]
    return render_template('accounts.html', accounts=accounts, title="Accounts")

@app.route('/add_account', methods=['POST', 'GET'])
def add_account():
    if request.method == 'POST':
        flash("TODO: submit account info")
        return redirect(url_for('accounts'))
    return render_template('add_account.html', title="Accounts")

def _make_options():
    class Option:
        def __init__(self, value):
            self.value = value
            self.description = value
    return [Option("Date"),
            Option("Withdrawal"),
            Option("Deposit"),
            Option("Description"),
            Option("Number")]


@app.route('/import_transactions', methods=['POST', 'GET'])
def import_transactions():
    lines = None
    selections = None
    if request.method == 'POST':
        try:
            file = request.files['file']
            if file:
                lines = [line for line in csv.reader(file)]
                max_length = 0
                for line in lines:
                    max_length = max(max_length, len(line))
                
                if 'selections' in request.form:
                    selections = request.form['selections']
                else:
                    selections = ["Empty"] * max_length
            else:
                flash("File was not uploaded")
        except Exception as e:
            flash("Exception: %s" % e)
            
    options = _make_options()

    return render_template('import_transactions.html', lines=lines, selections=selections, options=options, title="Transactions")


@app.route('/rules', methods=['POST', 'GET'])
def rules():
    if request.method == 'POST':
        flash('TODO')
        pass
    return render_template('rules.html', title="Rules")


if __name__ == "__main__":
    app.run()
