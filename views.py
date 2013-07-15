from personal_ledger import app
from models import *
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import csv

from categorize import categorize_expenses, categorize_columns, CATEGORIZE_COLUMN_OPTIONS

@app.route('/')
def index():
    return redirect(url_for('accounts'))

@app.route('/transactions')
def transactions():
    transactions = Transaction.query.all()
    return render_template('transactions.html', transactions=transactions, title="Transactions")

@app.route('/accounts')
def accounts():
    accounts = Account.query.order_by(Account.full_title)
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
        rule = Rule(regex, Account.query())
        db.session.add(rule)
        db.session.commit()
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
            
        select_columns = categorize_columns(lines)
        select_expenses = categorize_expenses(lines)
    else:
        flash("File was not uploaded")

    return render_template('categorize_transactions.html', lines=lines, select_columns=select_columns,
                           select_expenses=select_expenses, options=[title for title, item in CATEGORIZE_COLUMN_OPTIONS])
    
    
