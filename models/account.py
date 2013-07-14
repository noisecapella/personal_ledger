from personal_ledger import db

class Account(db.Model):
    id = db.Column(db.Integer, autoincrement = True, primary_key=True)
    title = db.Column(db.Text, unique=True, nullable=False)
    full_title = db.Column(db.Text, unique=True, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)
    
    parent = db.relation('Account', remote_side=[id])

    def __init__(self, title, parent):
        self.title = title
        self.parent = parent

        if parent:
            self.full_title = parent.full_title + " - " + title
        else:
            self.full_title = title
