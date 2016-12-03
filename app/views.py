from flask import render_template
from flask import request
from app import app
from .forms import PitcherForm, BatterForm, InjuryForm, WindowForm
from stats import batter as b
from injury import injury

@app.route('/')
@app.route('/index')
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


@app.route('/injury/batter')
def batter():
    inj_id = request.args.get("inj_id")
    window = request.args.get("window")

    inj = injury.get_injury(inj_id)
    s = b.prepost_aggregate_stats(int(inj_id), int(window))

    pre_slash = "/".join((format(s["pre"]["AVG"], '.3f').lstrip("0"), format(s["pre"]["OBP"], '.3f').lstrip("0"), format(s["pre"]["SLG"], '.3f').lstrip("0")))
    post_slash = "/".join((format(s["post"]["AVG"], '.3f').lstrip("0"), format(s["post"]["OBP"], '.3f').lstrip("0"), format(s["post"]["SLG"], '.3f').lstrip("0")))
    return render_template('batter.html', title='Batter', pre_slash=pre_slash, post_slash=post_slash)
