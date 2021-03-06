from loader import db

class Account(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.Text, unique=True, nullable=False)
    full_title = db.Column(db.Text, unique=True, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=True)
    
    def __init__(self, title, parent):
        self.title = title

        if parent:
            self.parent = parent

            self.full_title = parent.full_title + " - " + title
        else:
            self.full_title = title

class Rule(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    rule_type = db.Column(db.Text, nullable=False)
    regex = db.Column(db.Text, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    weight = db.Column(db.Float, nullable=False)

    use_description = "use_description"
    use_amount = "use_amount"

    def __init__(self, rule_type, regex, account, weight):
        if rule_type != self.use_amount and rule_type != self.use_description:
            raise Exception("Unknown rule_type")
        self.rule_type = rule_type
        self.regex = regex
        self.account = account
        self.weight = weight

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=False)
    withdrawal = db.Column(db.Float, nullable=False)
    deposit = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    other_transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)

    def __init__(self, description, withdrawal, deposit, account, date):
        if not withdrawal and not deposit:
            raise Exception("Must have a non-zero withdrawal or deposit")

        self.description = description
        self.withdrawal = withdrawal
        self.deposit = deposit
        self.account = account
        self.date = date
        # note that other_transaction must be set before committing

Transaction.account = db.relation('Account', backref='transaction')
Transaction.other_transaction = db.relation(Transaction, remote_side=[Transaction.id], uselist=False)


Rule.account = db.relation('Account', backref='rule')

Account.parent = db.relation('Account', remote_side=[Account.id])

