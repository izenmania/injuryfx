from db import connect
from injury import injury
import numpy
import pandas
import batter, graphics, player

def heatmap_coordinates(inj_id, window):
    # TODO: Provide a list of two sets of coordinates to be passed to graphics.generate_heatmap
    # window is the number of pitches in each direction to retrieve
    # Use injury.load_injury(inj_id, (player_id_mlbam, start_date, end_date)) to get details
    # Use two calls to get_pitches with the player id,  dates from load_injury, and the window value (one positive, one negative)
    pass


def get_pitches(pitcher_id, date, count, columns=()):
    # TODO: return a list of pitch events starting from a certain date
    # If count is negative, return that many before the date. Otherwise, after (including the date itself).
    # If columns is empty, return all columns from the pitch table. Otherwise, only those specified.
    pass


def get_atbats(pitcher_id, date, count, columns=()):
    # TODO: return a list of atbat events starting from a certain date
    # If count is negative, return that many before the date. Otherwise, after (including the date itself).
    # If columns is empty, return all columns from the atbat table. Otherwise, only those specified.
    pass

def get_pitches(player_id, date, count):
    conn = connect.sqlalchemy_open()

    if count < 0:
        operator = "<"
    else:
        operator = ">="
    sql = '''select pitch_type, count(game_id) pitch_count
             from (select game_id, pitch_type
                   from gameday.pitch 
                   where pitcher = %s
                   and substring(game_id, 1, 10) %s '%s'
                   LIMIT %s) p
             group by p.pitch_type''' \
                 % (player_id, operator, date.strftime("%Y/%m/%d"), abs(count))

    return pandas.read_sql_query(sql, conn)

def get_prepost_pitch_selection_histogram(injury_id, window):
    '''Create graph comparing of pitch selection before and after an injury'''

    max_window_size = int(injury.get_max_pitch_window(injury_id))
    if window > max_window_size:
        window = max_window_size

    inj = injury.get_injury(injury_id)
    pre = get_pitches(inj["player_id_mlbam"], inj["start_date"], window*-1)
    post = get_pitches(inj["player_id_mlbam"], inj["start_date"], window)
    return graphics.create_bar_chart(pre, post, injury_id, window)

