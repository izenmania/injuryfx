from flask import render_template, make_response, send_file
from flask import request
from app import app
from .forms import PitcherForm, BatterForm, InjuryForm, WindowForm
from stats import batter as b
from stats import pitcher as p
from stats import player as pl
from injury import injury
import StringIO
from datetime import datetime, date
import random

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from stats import graphics

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

@app.route('/preplot/')
def preplot():

    # Create the image object
    fig = graphics.generate_heatmap(1)

    # Create a fake file
    canvas = FigureCanvas(fig)
    output = StringIO.StringIO()
    fig.savefig(output)
    output.seek(0)
    return send_file(output, mimetype='image/png')


@app.route('/postplot/')
def postplot():

    # Create the image object
    fig = graphics.generate_heatmap(1)

    # Create a fake file
    canvas = FigureCanvas(fig)
    output = StringIO.StringIO()
    fig.savefig(output)
    output.seek(0)
    return send_file(output, mimetype='image/png')

@app.route('/injury/batter')
def batter():
    inj_id = request.args.get("inj_id")
    window = request.args.get("window")

    inj = injury.get_injury(inj_id)
    s = b.prepost_aggregate_stats(int(inj_id), int(window))

    pre = {
        "stats": "Slash Line: "+b.slash_line(s["pre"]),
        "image_path": "/static/images/figure_1.png"
    }
    post = {
        "stats": "Slash Line: "+b.slash_line(s["post"]),
        "image_path": "/static/images/figure_1.png"
    }

    # inj = {
    #     "first_name": "Bryce",
    #     "last_name": "Harper",
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

    return render_template('prepost.html', title='Batter', pre=pre, post=post, player=inj)


@app.route('/injury/pitcher')
def pitcher():
    inj_id = request.args.get("inj_id")
    window = request.args.get("window")

    inj = injury.get_injury(inj_id)
    s = p.prepost_aggregate_opp_stats(int(inj_id), int(window))

    pre = {
        "stats": "Opposing Slash Line: "+b.slash_line(s["pre"]),
        "image_path": "/static/images/figure_1.png"
    }
    post = {
        "stats": "Opposing Slash Line: "+b.slash_line(s["post"]),
        "image_path": "/static/images/figure_1.png"
    }

    return render_template('prepost.html', title='Pitcher', pre=pre, post=post, player=inj)



#[{'dl_type': '60-day', 'first_name': 'Tyler', 'last_name': 'Flowers', 'end_date': datetime.date(2013, 10, 24), 'start_date': datetime.date(2013, 9, 3), 'parts': [u'shoulder'], 'injury_id': 11957L, 'team_id_mlbam': 145L, 'injury': 'right shoulder surgery', 'side': 'right', 'player_id_mlbam': 452095L}, {'dl_type': '15-day', 'first_name': 'Tyler', 'last_name': 'Flowers', 'end_date': datetime.date(2016, 8, 17), 'start_date': datetime.date(2016, 7, 10), 'parts': [u'hand'], 'injury_id': 13330L, 'team_id_mlbam': 144L, 'injury': 'fractured left hand', 'side': 'left', 'player_id_mlbam': 452095L}]

@app.route('/player')
def player():
    player_id = request.args.get("player_id")

    split = pl.split_type(player_id)

    p = {
        "first_name": "Tyler",
        "last_name": "Flowers",
        "player_id": 452095
    }

    i = injury.get_player_injuries(player_id)

    return render_template('player_injury_list.html', title='Player', player=p, injuries=i, split=split)
