from flask import render_template
from myapp import myapp
from .forms import PitcherForm, BatterForm, InjuryForm, WindowForm

@myapp.route('/')
@myapp.route('/index')
def index():
    # Create form objects
    pitcherform = PitcherForm()
    batterform = BatterForm()
    injuryform = InjuryForm()
    windowform = WindowForm()

    # Render the template!
    return render_template('index.html',
                           title='Home',
			   pitcherform = pitcherform,
			   batterform = batterform,
			   injuryform = injuryform,
			   windowform = windowform)
