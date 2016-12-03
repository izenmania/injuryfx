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

    pre = {}
    post = {}

    pre["stats"] = b.slash_line(s["pre"])
    post["stats"] = b.slash_line(s["post"])
    pre["image_path"] = "/static/images/figure_1.png"
    post["image_path"] = "/static/images/figure_1.png"

    # inj = {
    #     "player_name": "Bryce Harper",
    #     "injury": "strained hamstring",
    #     "parts": ["leg"],
    #     "start_date": "7/13/2016",
    #     "end_date": "8/4/2016"
    # }
    # pre = {}
    # post = {}
    # pre["image_path"] = "/static/images/figure_1.png"
    # pre["stats"] = "Things"
    # post["image_path"] = "/static/images/figure_1.png"
    # post["stats"] = "Stuff"

    return render_template('batter.html', title='Batter', pre=pre, post=post, inj=inj)
