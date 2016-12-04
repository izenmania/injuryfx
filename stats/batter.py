from db import connect
from db import query
from injury import injury
import player
from datetime import datetime
import numpy
import pandas
import MySQLdb

# These functions are a lot like those in pitcher, but pull events based on the batter rather than pitcher
# Additionally, some of the functions include a "result" field.
# This is intended to let us get only pitches that the batter swings at, or only those that he makes contact with, etc.


def prepost_heatmap_coordinates(inj_id, window, result=""):
    # TODO: Provide a list of two sets of coordinates to be passed to graphics.generate_heatmap
    # window is the number of pitches in each direction to retrieve
    # Use injury.load_injury(inj_id, (player_id_mlbam, start_date, end_date)) to get details <-- there is no "load_injury"
    # Use two calls to get_pitches with the player id,  dates from load_injury, and the window value (one positive, one negative)

    inj_dates = injury.get_injury(inj_id)

    strt_dte = inj_dates['start_date']
    end_dte = inj_dates['end_date']
    plyr_id = inj_dates['player_id_mlbam']

    neg_window = window*(-1)


    pre_inj = get_pitches(plyr_id, strt_dte, neg_window)
    post_inj = get_pitches(plyr_id, end_dte, window)

    return pre_inj, post_inj


def get_pitches(batter_id, date, count, columns=(), result=""):
    # TODO: return a list of pitch events starting from a certain date
    # If count is negative, return that many before the date. Otherwise, after (including the date itself).
    # If columns is empty, return all columns from the pitch table. Otherwise, only those specified.
    if count < 0:
        operator = "<"
    else:
        operator = ">="

    conn = connect.open()

    sql = '''
        SELECT p.px AS x, p.pz AS y
        FROM gameday.game g
            INNER JOIN  gameday.pitch p ON g.game_id=p.game_id
        WHERE p.batter = %s AND g.date __operator__ %s
        ORDER BY g.date ASC
        LIMIT %s
    '''
    sql = sql.replace("__operator__", operator)
    params =  (batter_id, date.strftime("%Y-%m-%d"), abs(count))

    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, params)

    return_list = list(cur.fetchall())

    return return_list


def get_atbats(batter_id, date, count, columns=()):
    # TODO: return a list of atbat events starting from a certain date
    # If count is negative, return that many before the date. Otherwise, after (including the date itself).
    # If columns is empty, return all columns from the atbat table. Otherwise, only those specified.

    if count < 0:
        operator = "<"
    else:
        operator = ">="

    conn = connect.open()

    sql = '''
        SELECT g.date, ab.event
        FROM gameday.game g
            INNER JOIN JOIN gameday.atbat ab ON g.game_id=ab.game_id
        WHERE ab.batter = %s AND g.date __operator__ %s
        ORDER BY g.date DESC LIMIT %s
    '''
    sql = sql.replace("__operator__", operator)

    params = (batter_id, date.strftime("%Y-%m-%d"), abs(count))

    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, params)

    return_list = list(cur.fetchall())

    return return_list
