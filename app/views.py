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
        s = pl.prepost_aggregate_stats(int(inj_id), int(window))

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
        s = pl.prepost_aggregate_opp_stats(int(inj_id), int(window))

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


@app.route('/injury/pitches')
def injury_pitches():
    pass


@app.route('/injury/atbats')
def injury_atbats():
    inj_id = request.args.get("inj_id")
    window = request.args.get("window")

    inj = injury.get_injury(inj_id)

    if inj:
        player_type = pl.split_type(inj["player_id_mlbam"])
        s = pl.prepost_aggregate_stats(int(inj_id), int(window))

        if s["pre"] and s["post"]:
            if player_type == "batter":
                pre = {
                    "stats": "Slash Line: " + pl.slash_line(s["pre"]),
                    "image_path": "/static/images/figure_1.png"
                }
                post = {
                    "stats": "Slash Line: " + pl.slash_line(s["post"]),
                    "image_path": "/static/images/figure_1.png"
                }
            else:
                pre = {
                    "stats": "Opposing Slash Line: " + pl.slash_line(s["pre"]),
                    "image_path": "/static/images/figure_1.png"
                }
                post = {
                    "stats": "Opposing Slash Line: " + pl.slash_line(s["post"]),
                    "image_path": "/static/images/figure_1.png"
                }

            return render_template('prepost.html', title='Injury', pre=pre, post=post, player=inj)
        else:
            return render_template('error.html', title='Insufficient data', message='Insufficient data for this query.')
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


@app.route('/graphs/pitchselection')
def graph_pitch_selection():
    injury_id = int(request.args.get("injury_id"))
    window = int(request.args.get("window"))

    # Create the image object
    fig = p.get_prepost_pitch_selection_histogram(injury_id, window)

    return send_file(graphics.generate_fake_file(fig), mimetype='image/png')

@app.route('/injury/pitchselection')
def pitch_selection():
    injury_id = int(request.args.get("injury_id"))
    window = int(request.args.get("window"))

    inj = injury.get_injury(injury_id)
    if inj:
       return render_template('pitch_selection.html', title='Pitch Selection', window=window, player=inj)
    else:
       return render_template('error.html', title='Injury not found', message='No matching injury was found.')

