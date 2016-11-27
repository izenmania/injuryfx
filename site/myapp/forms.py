from flask.ext.wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

# Form classes for entering players and injuries
class PitcherForm(Form):
    pitcher = StringField('pitcher', validators=[DataRequired()])

class BatterForm(Form):
    batter = StringField('batter', validators=[DataRequired()])

class InjuryForm(Form):
    injury = StringField('injury', validators=[DataRequired()])

class WindowForm(Form):
    window = IntegerField('window',validators=[DataRequired()])
