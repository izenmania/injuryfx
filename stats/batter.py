from db import connect
from db import query
from injury import injury
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
    post_inj = get_pitchs(plyr_id, end_dte, window)

    return pre_inj, post_inj


def prepost_aggregate_stats(inj_id, window):
    # Retrieve the injury details
    inj = injury.get_injury(inj_id)

    # Generate aggregate stats for window days before and after the injury
    stats = {
        "pre": aggregate_stats(aggregatable_stats_window(inj["player_id_mlbam"], inj["start_date"], window*-1)),
        "post": aggregate_stats(aggregatable_stats_window(inj["player_id_mlbam"], inj["end_date"], window))
    }

    return stats


def get_pitches(batter_id, date, count, columns=(), result=""):
    # TODO: return a list of pitch events starting from a certain date
    # If count is negative, return that many before the date. Otherwise, after (including the date itself).
    # If columns is empty, return all columns from the pitch table. Otherwise, only those specified.
    if count < 0:
        operator = "<"
    else:
        operator = ">="

    conn = connect.open()

    sql = '''SELECT pitch.x, pitch.y FROM game JOIN pitch ON game.game_id=pitch.game_id WHERE pitch.batter = %s AND game.date %s '%s' ORDER BY game.date DESC LIMIT %s'''
    params =  (batter_id, operator, date.strftime("%Y-%m-%d"), abs(count))

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

    sql = '''SELECT game.date, atbat.event FROM game JOIN atbat ON game.game_id=atbat.game_id WHERE atbat.batter = %s AND game.date %s '%s' ORDER BY game.date DESC LIMIT %s'''

    params = (batter_id, operator, date.strftime("%Y-%m-%d"), abs(count))

    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, params)

    return_list = list(cur.fetchall())

    return return_list



def aggregate_stats(stats):
    agg = {
        "AB": stats["AB"].sum(),
        "PA": stats["PA"].sum(),
        "1B": stats["1B"].sum(),
        "2B": stats["2B"].sum(),
        "3B": stats["3B"].sum(),
        "HR": stats["HR"].sum(),
        "BB": stats["BB"].sum(),
        "IBB": stats["IBB"].sum(),
        "SO": stats["SO"].sum(),
        "SH": stats["SH"].sum(),
        "SF": stats["SF"].sum(),
        "HBP": stats["HBP"].sum(),
    }

    agg["AVG"] = round(float(agg["1B"]+agg["2B"]+agg["3B"]+agg["HR"])/float(agg["AB"]), 3)
    agg["OBP"] = round(float(agg["1B"]+agg["2B"]+agg["3B"]+agg["HR"]+agg["BB"]+agg["IBB"]+agg["HBP"])/float(agg["PA"]), 3)
    agg["SLG"] = round(float(agg["1B"]+2*agg["2B"]+3*agg["3B"]+4*agg["HR"])/float(agg["AB"]), 3)
    agg["OPS"] = agg["OBP"] + agg["SLG"]

    return agg


def aggregatable_stats_window(batter_id, date, count):
    # TODO: return player aggregate stats over the specified window.
    conn = connect.sqlalchemy_open()

    if count < 0:
        operator = "<"
    else:
        operator = ">="
    sql = "SELECT * FROM aggregate_batting WHERE batter = %s AND date %s '%s' ORDER BY game_id, inning, num LIMIT %s" % (batter_id, operator, date.strftime("%Y-%m-%d"), abs(count))

    return pandas.read_sql_query(sql, conn)


# Take a the results of aggregate_stats and return a slash line (avg/obp/slg) in text format
def slash_line(agg_stats):
    return "/".join((format(agg_stats["AVG"], '.3f').lstrip("0"),
                     format(agg_stats["OBP"], '.3f').lstrip("0"),
                     format(agg_stats["SLG"], '.3f').lstrip("0")))
