class Column:
    def __init__(self, name, type, autoincrement=False, notnull=False, primarykey=False):
        self.name = name
        if type == int:
            self.type = "integer"
        elif type == str:
            self.type = "text"
        elif type == float:
            self.type = "float"
        else:
            raise Exception("Unhandled type error")
        self.autoincrement = autoincrement
        self.notnull = notnull
        self.primarykey = primarykey

    def make_description(self):
        s = "%s %s" % (self.name, self.type)
        if self.primarykey:
            s += " PRIMARY KEY"
        if self.notnull:
            s += " NOT NULL"
        if self.autoincrement:
            s += " AUTOINCREMENT"
        return s
        
def create_schema():
    class Accounts:
        tablename = "accounts"

        def __init__(self):
            self.columns = [Column("id", int, autoincrement=True, primarykey=True),
                            Column("title", str, notnull=True),
                            Column("full_title", str, notnull=True),
                            Column("parent_id", int)]

    class Transactions:
        tablename = "transactions"

        def __init__(self):
            self.columns = [Column("id", int, autoincrement=True, primarykey=True),
                            Column("description", str, notnull=True),
                            Column("withdrawal", float, notnull=True),
                            Column("deposit", float, notnull=True),
                            Column("account_id", int, notnull=True),
                            Column("other_transaction_id", int, notnull=True)]
            
    
    tables = [Transactions(), Accounts()]

    for table in tables:
        print "DROP TABLE IF EXISTS %s;" % table.tablename
        print "CREATE TABLE %s (" % table.tablename
        print ",\n".join(column.make_description() for column in table.columns)
        print ");"
        print

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
                            'Water':None}}}
    write_account_tree(account_tree)

def write_account_tree(account_tree, this_id = 0, parent_id = None, parent_title_stack = ""):
    start_index = this_id
    if account_tree is None:
        return 0
    if parent_id is None:
        parent_str = "NULL"
    else:
        parent_str = str(parent_id)

    for name, children in account_tree.iteritems():
        if parent_title_stack:
            full_title = parent_title_stack + " - " + name
        else:
            full_title = name
        print "INSERT INTO ACCOUNTS (id, title, parent_id, full_title) VALUES (%d, '%s', %s, '%s');" % (start_index, name, parent_str, full_title)
        start_index += 1
        start_index += write_account_tree(children, start_index, start_index - 1, full_title)
        
    return start_index - this_id
if __name__ == "__main__":
    create_schema()
