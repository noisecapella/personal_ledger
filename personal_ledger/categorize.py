import dateutil.parser
import re

from models import *

class DateOption:
    title = "Date"
    def validate(self, s):
        try:
            dateutil.parser.parse(s)
            return True
        except ValueError:
            return False

    def parse(self, s):
        return dateutil.parser.parse(s)

class DescriptionOption:
    title = "Description"
    def validate(self, s):
        return True

    def parse(self, s):
        return s

class DepositOption:
    title = "Deposit"
    def validate(self, s):
        return re.match("\d+\.\d\d", s)

    def parse(self, s):
        return float(s)

class WithdrawalOption:
    title = "Withdrawal"
    def validate(self, s):
        return re.match("\d+\.\d\d", s)

    def parse(self, s):
        return float(s)

CATEGORIZE_COLUMN_OPTIONS = [DateOption(),
                             DescriptionOption(),
                             WithdrawalOption(),
                             DepositOption()]

CATEGORIZE_COLUMN_OPTIONS_KEYS = {option.title: option for option in CATEGORIZE_COLUMN_OPTIONS}
                                  
def guess(line):
    matches_made = [None] * len(line)

        
    # TODO: reimplement with efficient algorithm
    # probably not important given the small number of validations
    validations = {title: [bool(option.validate(c)) for c in line]
                   for title, option in CATEGORIZE_COLUMN_OPTIONS_KEYS.items()}

    while not all(matches_made):
        validation_counts = [0] * len(line)
        for title, validation_row in validations.items():
            for i in xrange(len(line)):
                if validation_row[i]:
                    validation_counts[i] += 1


        max_validation_index = None
        for i in xrange(len(line)):
            if matches_made[i]:
                continue
            elif max_validation_index is None:
                max_validation_index = i
            elif validation_counts[max_validation_index] > validation_counts[i]:
                max_validation_index = i

        for title, row in validations.items():
            if row[max_validation_index]:
                matches_made[max_validation_index] = CATEGORIZE_COLUMN_OPTIONS_KEYS[title]

                break
        else:
            raise Exception("No match made this round")

        for title, row in validations.items():
            row[max_validation_index] = False

        for i in xrange(len(line)):
            validations[matches_made[max_validation_index].title][i] = False

    return matches_made

def categorize_expenses(lines, column_options):
    rules = Rule.query.all()
    default_account = Account.query.filter(Account.title == "Uncategorized").first()

    description_index = None
    amount_index = None
    for i, column_option in enumerate(column_options):
        if column_option.title == DescriptionOption.title:
            description_index = i
        elif column_option.title == DepositOption.title or column_option.title == WithdrawalOption.title:
            amount_index = i

    if description_index is None or amount_index is None:
        raise Exception("No description column found")

    def best_match(line):
        # for now any match is a good match
        # TODO: make this better

        match_account = None
        matched_rule = None
        for rule in rules:
            if rule.rule_type == Rule.use_description:
                item = line[description_index]
            elif rule.rule_type == Rule.use_amount:
                item = line[amount_index]
            else:
                raise Exception("Unable to find rule type")
            #print("Attempting " + rule.regex + " against " + item)
            if rule.regex.lower() in item.lower():
                if match_account is not None:
                    #raise Exception("Multiple matches found. First account was %s, second account was %s. Previous regex was %s, current regex is %s, item is %s" % (match_account.full_title, rule.account.full_title, matched_rule.regex, rule.regex, item))
                    return None
                matched_rule = rule
                match_account = rule.account
        return match_account
            

    ret = [(best_match(line) or default_account)
           for line in lines]

    return ret
        
        


def categorize_columns(lines):
    if not lines:
        return list()
    
    return guess(lines[0])


