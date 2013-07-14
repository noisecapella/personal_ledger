from personal_ledger import db
from account import Account

class Rule(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    regex = db.Column(db.Text, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    account = db.relation('Account', remote_side=[Account.id])

    def __init__(self, regex, account):
        self.regex = regex
        self.account = account
