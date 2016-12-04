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

    if inj:
        s = b.prepost_aggregate_stats(int(inj_id), int(window))

        pre = {
            "stats": "Slash Line: "+b.slash_line(s["pre"]),
            "image_path": "/static/images/figure_1.png"
        }
        post = {
            "stats": "Slash Line: "+b.slash_line(s["post"]),
            "image_path": "/static/images/figure_1.png"
        }

        return render_template('prepost.html', title='Batter', pre=pre, post=post, player=inj)

    else:
        return render_template('error.html', title='Injury not found.', message='No matching injury was found.')


@app.route('/injury/pitcher')
def pitcher():
    inj_id = request.args.get("inj_id")
    window = request.args.get("window")

    inj = injury.get_injury(inj_id)

    if inj:
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

    else:
        return render_template('error.html', title='Injury not found.', message='No matching injury was found.')


@app.route('/player')
def player():
    player_id = request.args.get("player_id")
    year = request.args.get("year")

    if player_id:
        p = pl.get_player(player_id)
        if p:
            split = pl.split_type(player_id)
            i = injury.get_player_injuries(player_id)

            return render_template('player_injury_list.html', title='Player', player=p, injuries=i, split=split)
        else:
            return render_template('error.html', title='Player not found', message='No matching player was found.')
    else:
        pitchers = pl.all_players_with_injuries("pitcher", year=year)
        batters = pl.all_players_with_injuries("batter", year=year)

        return render_template('players_all.html', title='Players', pitchers=pitchers, batters=batters)


@app.route('/error')
def error():
    return render_template('error.html', title='Error', message="This is an error message.")