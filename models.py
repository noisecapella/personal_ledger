from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Account(db.Model):
    id = db.Column(db.Integer, autoincrement = True, primary_key=True)
    title = db.Column(db.Text, unique=True, nullable=False)
    full_title = db.Column(db.Text, unique=True, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)
    
    def __init__(self, title, parent):
        self.title = title

        if parent:
            self.parent = parent

            self.full_title = parent.full_title + " - " + title
        else:
            self.full_title = title

class Rule(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    regex = db.Column(db.Text, nullable=False)

    def __init__(self, regex, account):
        self.regex = regex
        self.account = account

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=False)
    withdrawal = db.Column(db.Float, nullable=False)
    deposit = db.Column(db.Float, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    other_transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)

    def __init__(self, description, withdrawal, deposit, account):
        if not withdrawal and not deposit:
            raise Exception("Must have a non-zero withdrawal or deposit")

        self.description = description
        self.withdrawal = withdrawal
        self.account = account
        # note that other_transaction must be set before committing

Transaction.account = db.relation('Account', backref='transaction')
Transaction.other_transaction = db.relation(Transaction, backref='transaction', uselist=False)


Rule.account = db.relation('Account', backref='rule')

Account.parent = db.relation('Account', backref='account')

