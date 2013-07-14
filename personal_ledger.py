import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import csv
from contextlib import closing

from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)

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
        except Exception as e:
            flash("Exception: %s" % e)
            
    options = _make_options()

    return render_template('import_transactions.html', lines=lines, selections=selections, options=options, title="Transactions")


@app.route('/rules', methods=['GET', 'POST'])
def rules():
    if request.method == "POST":
        regex = request.form['regex']
        account_id = request.form['account_id']
        #cur = g.db.execute('INSERT INTO rules ?, ?', 
        #TODO
        return redirect(url_for('rules'))

    cur = g.db.execute('SELECT regex, accounts.full_title FROM rules JOIN accounts ON rules.account_id == accounts.id')
    rules = [dict(regex=row[0], account=row[1]) for row in cur.fetchall()]
    return render_template('rules.html', title="Rules", rules=rules)

@app.route('/categorize_transactions', methods=['POST'])
def categorize_transactions():
    file = request.files['file']
    if file:
        lines = [line for line in csv.reader(file)]
        max_length = 0
        for line in lines:
            max_length = max(max_length, len(line))
            
    else:
        flash("File was not uploaded")

    return render_template('categorize_transactions.html', lines=lines)
    
    
if __name__ == "__main__":
    app.run()
