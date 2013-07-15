import dateutil.parser
import re

from models import *

class DateOption:
    title = "Date"
    def validate(self, s):
        try:
            dateutil.parser.parse(s)
            return True
        except:
            return False

    def parse(self, s):
        return dateutil.parser.parse(s)

class DescriptionOption:
    title = "Description"
    def validate(self, s):
        return True

    def parse(self, s):
        return s

class MoneyOption:
    title = "Money"
    def validate(self, s):
        return re.match("\d+\.\d\d", s)

    def parse(self, s):
        return float(s)

CATEGORIZE_COLUMN_OPTIONS = [DateOption(),
                             DescriptionOption(),
                             MoneyOption()]

CATEGORIZE_COLUMN_OPTIONS_KEYS = {option.title: option for option in CATEGORIZE_COLUMN_OPTIONS}
                                  
def guess(line):
    matches_made = [None] * len(line)

        
    # TODO: reimplement with efficient algorithm
    # probably not important given the small number of validations
    validations = {title: [bool(option.validate(c)) for c in line]
                   for title, option in CATEGORIZE_COLUMN_OPTIONS_KEYS.items()}
    print validations
    while not all(matches_made):
        validation_counts = [0] * len(line)
        for title, validation_row in validations.items():
            for i in xrange(len(line)):
                if validation_row[i]:
                    validation_counts[i] += 1

        min_validation_index = 0
        for i in xrange(len(line)):
            if validation_counts[min_validation_index] < validation_counts[i]:
                min_validation_index = i

        for title, row in validations.items():
            if row[min_validation_index]:
                matches_made[min_validation_index] = CATEGORIZE_COLUMN_OPTIONS_KEYS[title]

                break
        else:
            raise Exception("No valid items")

        for title, row in validations.items():
            row[min_validation_index] = False



    return matches_made

def categorize_expenses(lines, column_options):
    rules = Rule.query.all()
    default_account = Rule.query.first().account

    index = None
    for i, column_option in enumerate(column_options):
        if column_option.title == DescriptionOption.title:
            index = i
            break
    else:
        print("No description column found")
        return [default_account] * len(lines)

    def best_match(regex, item):
        # for now any match is a good match
        # TODO: make this better
        for rule in rules:
            if re.match(rule.regex, item):
                return rule.account
            

    ret = [(best_match(line[index]) or default_account)
           for line in lines]

    return ret
        
        


def categorize_columns(lines):
    if not lines:
        return []
    
    return guess(lines[0])


