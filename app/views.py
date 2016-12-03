from flask import render_template
from flask import request
from app import app
from .forms import PitcherForm, BatterForm, InjuryForm, WindowForm
from stats import batter

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

    s = batter.prepost_aggregate_stats(int(inj_id), int(window))

    #pre_slash = stats["pre"]
    #post_slash = stats["post"]
    return render_template('batter.html', title='Batter', pre_slash=inj_id, post_slash=window)