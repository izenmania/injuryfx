from flask import render_template, make_response, send_file
from flask import request
from app import app
from .forms import PitcherForm, BatterForm, InjuryForm, WindowForm
from stats import batter as b
from stats import pitcher as p
from stats import player as pl
from stats import injury
import StringIO
from datetime import datetime, date
import random

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from stats import graphics

@app.route('/')
@app.route('/index')
def index():
    """Flask view for the application home page."""

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

@app.route('/team')
def team():
    """Flask view for the development team bios"""
    return render_template('team.html', title='Team')

@app.route('/injury/pitches')
def injury_pitches():
    """Flask view for pitch-location heatmaps before and after an injury. Used for both pitchers and batters."""
    inj_id = request.args.get("inj_id")
    window = request.args.get("window")
    result = request.args.get("result")

    inj = injury.get_injury(inj_id)

    if inj:
        player_type = pl.split_type(inj["player_id_mlbam"])
        pre = {
            "header": "Pitches Thrown Pre-Injury" if player_type == "pitcher" else "Pitches Faced Pre-Injury",
            "footer": "",
            "image_path": "/graphs/heatmap?inj_id=%s&window=%s&side=pre&result=%s" % (inj_id, window, result)
        }
        post = {
            "header": "Pitches Thrown Post-Injury" if player_type == "pitcher" else "Pitches Faced Post-Injury",
            "footer": "",
            "image_path": "/graphs/heatmap?inj_id=%s&window=%s&side=post&result=%s" % (inj_id, window, result)
        }

        return render_template('prepost.html', title='Pitch Location', pre=pre, post=post, player=inj)
    else:
        return render_template('error.html', title='Injury not found.', message='No matching injury was found.')


@app.route('/injury/atbats')
def injury_atbats():
    """Flask view for at-bat level aggregate statistics, and eventually for spraychart outcome visualizations."""
    inj_id = request.args.get("inj_id")
    window = request.args.get("window")

    inj = injury.get_injury(inj_id)

    if inj:
        player_type = pl.split_type(inj["player_id_mlbam"])
        s = pl.prepost_aggregate_stats(int(inj_id), int(window))

        if s["pre"] and s["post"]:
            if player_type == "batter":
                pre = {
                    "header": "Offense Pre-Injury",
                    "footer": "Slash Line: " + pl.slash_line(s["pre"]),
                    "image_path": "/static/images/spraychart.png"
                }
                post = {
                    "header": "Offense Post-Injury",
                    "footer": "Slash Line: " + pl.slash_line(s["post"]),
                    "image_path": "/static/images/spraychart.png"
                }
            else:
                pre = {
                    "header": "Opposing Offense Pre-Injury",
                    "footer": "Slash Line: " + pl.slash_line(s["pre"]),
                    "image_path": "/static/images/spraychart.png"
                }
                post = {
                    "header": "Opposing Offense Post-Injury",
                    "footer": "Slash Line: " + pl.slash_line(s["post"]),
                    "image_path": "/static/images/spraychart.png"
                }

            return render_template('prepost.html', title='At Bats', pre=pre, post=post, player=inj)
        else:
            return render_template('error.html', title='Insufficient data', message='Insufficient data for this query.')
    else:
        return render_template('error.html', title='Injury not found.', message='No matching injury was found.')


@app.route('/player')
def player():
    """Flask view for individual or listing players"""
    player_id = request.args.get("player_id")
    year = request.args.get("year")

    if player_id:
        # If a player_id is specified, display a list of all injuries for that player, and links to visualizations.
        p = pl.get_player(player_id)
        if p:
            player_type = pl.split_type(player_id)
            inj = injury.get_player_injuries(player_id)

            for i in inj:
                max_pitch_window = injury.get_max_pitch_window(i["injury_id"])
                if max_pitch_window < 150:
                    i["pitch_window"] = max_pitch_window
                else:
                    i["pitch_window"] = 150

                max_atbat_window = injury.get_max_atbat_window(i["injury_id"])
                if max_atbat_window < 50:
                    i["atbat_window"] = max_atbat_window
                else:
                    i["atbat_window"] = 50

            return render_template('player_injury_list.html', title='Player', player=p, injuries=inj, player_type=player_type)
        else:
            return render_template('error.html', title='Player not found', message='No matching player was found.')
    else:
        # If no player_id, display a list of all pitchers and batters with viewable injury information.
        pitchers = pl.all_players_with_injuries("pitcher", year=year)
        batters = pl.all_players_with_injuries("batter", year=year)

        return render_template('players_all.html', title='Players', pitchers=pitchers, batters=batters)


@app.route('/error')
def error():
    """Generic Flask view for error pages"""
    return render_template('error.html', title='Error', message="This is an error message.")


@app.route('/graphs/pitchselection')
def graph_pitch_selection():
    """Flask view for generating pitch selection barcharts as an image in the browser"""
    injury_id = int(request.args.get("injury_id"))
    window = int(request.args.get("window"))

    # Create the image object
    fig = p.get_prepost_pitch_selection_histogram(injury_id, window)

    return send_file(graphics.generate_fake_file(fig), mimetype='image/png')

@app.route('/injury/pitchselection')
def pitch_selection():
    """Flask view for displaying the pitch selection barchart image for a given injury event."""
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
    """Flask view for generating pitch location heatmaps as an image in the browser."""
    inj_id = int(request.args.get("inj_id"))
    window = int(request.args.get("window"))
    side = request.args.get("side")
    result = request.args.get("result")

    if side == "pre":
        coef = -1
    else:
        coef = 1

    inj = injury.get_injury(inj_id)

    if inj:
        coords = pl.get_pitches(inj["player_id_mlbam"], inj["start_date"], coef * window, result=result)

        # Create the image object
        fig = graphics.generate_heatmap(coords)

        return send_file(graphics.generate_fake_file(fig), mimetype='image/png')
