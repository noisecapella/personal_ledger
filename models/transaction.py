from personal_ledger import db
from account import Account

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=False)
    withdrawal = db.Column(db.Float, nullable=False)
    deposit = db.Column(db.Float, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    other_transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)

    account = db.relation('Account', remote_side=[Account.id])
    other_transaction = db.relation('Transaction', remote_side=[id])

    def __init__(self, description, withdrawal, deposit, account):
        if not withdrawal and not deposit:
            raise Exception("Must have a non-zero withdrawal or deposit")

        self.description = description
        self.withdrawal = withdrawal
        self.account = account
        # note that other_transaction must be set before committing
