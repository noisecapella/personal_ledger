from wtforms import Form, validators, TextField, SelectField
from models import Account, Rule

class CreateRuleForm(Form):
    rule_type = SelectField('Type', [validators.Required()],
                            choices=[(Rule.use_description, "Match against description"),
                                     (Rule.use_amount, "Match against amount")])
    regex = TextField('Regular Expression', [validators.Required()])
    account_id = SelectField('Account', [validators.Required()],
                             choices=[(str(account.id), account.full_title) for account in Account.query.order_by(Account.full_title).all()])
    weight = TextField('Weight', [validators.Regexp('\d+')], default="1")
