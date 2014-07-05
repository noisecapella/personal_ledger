from loader import app
from models import *
from forms import *
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import csv
import re

import dateutil.parser

from sqlalchemy.sql.expression import func

from categorize import categorize_expenses, categorize_columns, CATEGORIZE_COLUMN_OPTIONS
import json

@app.route('/')
def index():
    return redirect(url_for('accounts'))

@app.route('/transactions')
def transactions():
    transactions = Transaction.query.order_by(Transaction.date.desc())
    return render_template('transactions.html', transactions=transactions, title="Transactions")

@app.route('/accounts')
def accounts():
    month_year = request.args.get('month_year')
    month_years = (db.session.query(func.strftime("%m-%Y", Transaction.date))
                   .select_from(Transaction)
                   .distinct()
                   .order_by(func.strftime("%Y-%m", Transaction.date))
                   .all()
                   )
    month_years = [each[0] for each in month_years]

    accounts_query = (db.session.query(
        func.sum(Transaction.withdrawal),
        func.sum(Transaction.deposit),
        Account.full_title)
                .select_from(Account)
                .outerjoin(Transaction)
                .group_by(Account.id)
                .order_by(Account.full_title)
                )

    if month_year:
        accounts_query = accounts_query.filter(func.strftime("%m-%Y", Transaction.date) == month_year)

    accounts = accounts_query.all()
                

    def relabel(account):
        return {"withdrawal": account[0],
                "deposit": account[1],
                "full_title": account[2]}
                
    accounts = [relabel(account) for account in accounts]
    return render_template('accounts.html', accounts=accounts, title="Accounts", month_year=month_year, month_years=month_years)
    

@app.route('/accounts/new', methods=['GET'])
def add_account():
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


@app.route('/import_transactions', methods=['GET'])
def import_transactions():
    lines = None
    selections = None

    options = _make_options()

    return render_template('import_transactions.html', lines=lines, selections=selections, options=options, title="Transactions")

@app.route('/rules/create', methods=['POST'])
def rules_create():
    form = CreateRuleForm(request.form)

    if form.validate():
        rule = Rule(form.rule_type.data,
                    form.regex.data,
                    Account.query.get(form.account_id.data),
                    form.weight.data)
        db.session.add(rule)
        db.session.commit()
        flash("New rule created")
    else:
        flash("Form error")
        raise Exception("Form errors: %s" % form.errors)

    return json.dumps({'html' : (render_template('categorize_transactions_partial.html') +
                                 render_template('categorize_transactions_partial_js.html'))})



@app.route('/rules', methods=['GET'])
def rules():
    rules = Rule.query.all()
    form = CreateRuleForm(request.form)
    return render_template('rules.html', title="Rules", rules=rules, form=form)



@app.route('/rules/new_partial', methods=['GET', 'POST'])
def rules_new_partial():
    form = CreateRuleForm(request.form)
    return render_template('add_rule_partial.html', title="Rules", form=form)

@app.route('/categorize_transactions', methods=['GET', 'POST'])
def categorize_transactions():
    if request.method == 'GET':
        return redirect(url_for('import_transactions'))
    file = request.files['file']
    if file:
        lines = [line for line in csv.reader(file)]

        select_columns = categorize_columns(lines)
        select_expenses = categorize_expenses(lines, select_columns)
    else:
        flash("File was not uploaded")
        return redirect(url_for('import_transactions'))

    options = CATEGORIZE_COLUMN_OPTIONS
    accounts = Account.query.order_by(Account.full_title).all()

    pairs = [(lines[i], select_expenses[i]) for i in xrange(len(lines))]

    def uncategorized_first(pair):
        if pair[1].title == "Uncategorized":
            return 0
        else:
            return 1

    pairs = sorted(pairs, key=uncategorized_first)

    return render_template('categorize_transactions.html', lines=lines, select_columns=select_columns,
                           pairs=pairs, options=options, accounts=accounts)


@app.route('/transactions/bulk_create', methods=['POST'])
def transactions_bulk_create():
    num_columns = int(request.form["num_columns"])
    source_account_id = request.form["source_account_id"]

    columns = {}
    for column_num in xrange(num_columns):
        columns[request.form["selection_" + str(column_num)]] = column_num


    num_transactions = int(request.form["num_transactions"])

    source_account = Account.query.get(source_account_id)
    for transaction_num in xrange(num_transactions):
        if "Description" in columns:
            description = request.form["cell_" + str(transaction_num) + "_" + str(columns["Description"])]
        else:
            description = "Unspecified description"

        if "Withdrawal" in columns:
            withdrawal = request.form["cell_" + str(transaction_num) + "_" + str(columns["Withdrawal"])]
        else:
            withdrawal = 0
        if "Deposit" in columns:
            deposit = request.form["cell_" + str(transaction_num) + "_" + str(columns["Deposit"])]
        else:
            deposit = 0
        if "Date" in columns:
            date_string = request.form["cell_" + str(transaction_num) + "_" + str(columns["Date"])]
        else:
            date_string = "01/01/1900"
        date = dateutil.parser.parse(date_string)

        other_account_id = request.form["select_expenses_" + str(transaction_num)]
        other_account = Account.query.get(other_account_id)
        transaction = Transaction(description, withdrawal, deposit, source_account, date)
        other_transaction = Transaction(description, deposit, withdrawal, other_account, date)

        # temporarily satisfy NOT NULL requirement
        transaction.other_transaction_id = -1
        other_transaction.other_transaction_id = -1

        db.session.add(transaction)
        db.session.add(other_transaction)
        db.session.flush()

        transaction.other_transaction_id = other_transaction.id
        other_transaction.other_transaction_id = transaction.id

        db.session.commit()

    return redirect(url_for(".transactions"))

@app.route('/transactions_partial', methods=['GET'])
def transactions_partial():
    transactions = Transaction.query.order_by(Transaction.date.desc())
    regex = request.args.get('regex')
    if regex:
        transactions = [transaction for transaction in transactions
                        if re.match(regex, transaction.description)]

    return render_template('transactions_partial.html', transactions=transactions)
        

