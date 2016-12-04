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


@app.route('/injury/pitches')
def injury_pitches():
    inj_id = request.args.get("inj_id")
    window = request.args.get("window")

    inj = injury.get_injury(inj_id)

    if inj:
        player_type = pl.split_type(inj["player_id_mlbam"])
        pre = {
            "stats": "",
            "image_path": "/graphs/heatmap"
        }
        post = {
            "stats": "",
            "image_path": "/graphs/heatmap"
        }

        return render_template('prepost.html', title='Pitch Location', pre=pre, post=post, player=inj)
    else:
        return render_template('error.html', title='Injury not found.', message='No matching injury was found.')


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

            return render_template('prepost.html', title='At Bats', pre=pre, post=post, player=inj)
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
            player_type = pl.split_type(player_id)
            i = injury.get_player_injuries(player_id)

            return render_template('player_injury_list.html', title='Player', player=p, injuries=i, player_type=player_type)
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

       max_window_size = int(injury.get_max_pitch_window(injury_id))
       if window > max_window_size:
          window = max_window_size

       if window > 0:
          return render_template('pitch_selection.html', title='Pitch Selection', window=window, player=inj)
       else: 
          return render_template('error.html', title='Window too small.', message='Pitch selection could not be calculated because either a non-positive window was specified or the max window size is 0')
    else:
       return render_template('error.html', title='Injury not found', message='No matching injury was found.')


@app.route('/graphs/heatmap')
def graph_heatmap():
    coords = [(-0.076, 1.472),(-0.940, 1.910),(-1.119, 2.892),(-0.181, 2.269),(-0.491, 2.104),(0.340, 2.302),(-1.057, 2.382),(-0.710, 1.016),(-0.791, 2.052),(-1.039, 2.814),(1.308, 1.178),(0.195, 1.263),(-0.692, 2.082),(0.376, 1.098),(0.137, 2.857),(1.413, 2.685),(-0.058, 1.343),(0.495, 2.381),(-0.222, 2.658),(0.779, 0.018),(0.459, 2.228),(1.237, 1.058),(0.737, 1.856),(0.096, 1.426),(-0.696, 3.452),(0.559, 1.340),(-1.893, 2.513),(-0.805, 3.600),(0.298, 1.846),(-0.297, 2.728),(-0.958, 3.237),(-0.159, 2.048),(0.373, 1.658),(0.663, 3.307),(0.891, 0.998),(1.295, 0.072),(-1.047, 2.789),(0.363, 2.663),(1.659, 0.994),(1.011, 1.433),(0.652, 2.080),(-0.970, 1.603),(1.202, 2.483),(0.662, 1.784),(-0.697, 3.288),(0.227, 3.408),(-2.961, 3.667),(0.803, 0.435),(-1.999, 3.351),(0.542, 4.356),(-0.257, 1.072),(-0.249, 2.562),(0.138, 3.004),(1.190, 0.468),(2.190, 0.580),(-0.582, 2.918),(1.209, 0.779),(0.805, 0.773),(0.036, 1.780),(1.119, 2.659),(-0.609, 2.606),(-0.084, 2.047),(0.222, 1.982),(0.002, 1.153),(0.985, 2.350),(1.051, 0.645),(1.202, 1.823),(0.447, 1.776),(0.135, 1.236),(0.080, 1.853),(-0.260, 1.927),(2.365, 2.978),(1.422, 0.693),(-0.931, 2.878),(1.352, 0.987),(1.254, 2.215),(-0.691, 2.400),(0.917, 2.274),(0.338, 1.983),(-1.326, 2.458),(-0.476, 2.700),(0.454, 0.566),(-0.137, 1.922),(-0.461, 2.140),(0.575, 1.472),(-1.203, 2.577),(-0.324, 2.946),(0.996, 3.123),(1.589, 2.433),(0.258, 3.007),(-0.537, 3.488),(1.571, 1.491),(0.725, 4.217),(0.458, 1.997),(0.588, 0.911),(0.027, 3.511),(0.138, 2.176),(-0.361, 1.603),(-1.135, 2.745),(-0.165, 2.907)]

    # Create the image object
    fig = graphics.generate_heatmap(coords)

    return send_file(graphics.generate_fake_file(fig), mimetype='image/png')