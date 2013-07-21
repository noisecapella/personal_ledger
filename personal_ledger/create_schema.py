from loader import db
from models import Account, Transaction, Rule

def create_schema():
    db.drop_all()
    db.create_all()
    
    account_tree = {"Assets" : {"Bank Savings" : None,
                                "Bank Checking" : None,
                                "Cash in Wallet" : None},
                    "Liabilities" : {"Credit Card" : None},
                    "Expenses" : {
                        'Bicycle':None,
                        'Books':None,
                        'Cable':None,
                        'Charity':None,
                        'Clothes':None,
                        'Computer':None,
                        'Dining':None,
                        'Education':None,
                        'Music/Movies':None,
                        'Recreation':None,
                        'Travel':None,
                        'Gifts':None,
                        'Groceries':None,
                        'Hobbies':None,
                        'Insurance': {
                            'Auto Insurance':None,
                            'Health Insurance':None,
                            'Life Insurance':None},
                        'Laundry/Dry Cleaning':None,
                        'Medical Expenses':None,
                        'Miscellaneous':None,
                        'Online Services':None,
                        'Phone':None,
                        'Public Transportation':None,
                        'Rent':None,
                        'Subscriptions':None,
                        'Supplies':None,
                        'Taxes': {
                            'Federal':None,
                            'Medicare':None,
                            'Other Tax':None,
                            'Social Security':None,
                            'State/Providence':None},
                        'Utilities': {
                            'Electric':None,
                            'Garbage collection':None,
                            'Gas':None,
                            'Water':None}},
                    "Uncategorized" : None}
    write_account_tree(account_tree)
    db.session.commit()

def write_account_tree(account_tree, parent = None):
    if not account_tree:
        return

    for name, children in account_tree.iteritems():
        account = Account(name, parent)
        db.session.add(account)
        write_account_tree(children, account)
if __name__ == "__main__":
    create_schema()
