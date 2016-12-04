from db import connect
from injury import injury
import numpy
import pandas
import batter, graphics
import MySQLdb

def heatmap_coordinates(inj_id, window):
    # TODO: Provide a list of two sets of coordinates to be passed to graphics.generate_heatmap
    # window is the number of pitches in each direction to retrieve
    # Use injury.load_injury(inj_id, (player_id_mlbam, start_date, end_date)) to get details
    # Use two calls to get_pitches with the player id,  dates from load_injury, and the window value (one positive, one negative)
    inj_dates = injury.get_injury(inj_id)

    strt_dte = inj_dates['start_date']
    end_dte = inj_dates['end_date']
    plyr_id = inj_dates['player_id_mlbam']

    neg_window = window*(-1)


    pre_inj = get_pitches(plyr_id, strt_dte, neg_window)
    post_inj = get_pitches(plyr_id, end_dte, window)

    return pre_inj, post_inj


def get_pitches(pitcher_id, date, count, columns=()):
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
            INNER JOIN gameday.pitch p ON g.game_id=p.game_id
        WHERE p.pitcher = %s AND
            g.date __operator__ %s
        ORDER BY g.date DESC LIMIT %s'''
    sql = sql.replace("__operator__", operator)

    params =  (pitcher_id, date.strftime("%Y-%m-%d"), abs(count))

    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, params)

    return_list = list(cur.fetchall())

    return return_list


def get_atbats(pitcher_id, date, count, columns=()):
    # TODO: return a list of atbat events starting from a certain date
    # If count is negative, return that many before the date. Otherwise, after (including the date itself).
    # If columns is empty, return all columns from the atbat table. Otherwise, only those specified.

    if count < 0:
        operator = "<"
    else:
        operator = ">="

    conn = connect.open()

    sql = '''SELECT game.date, atbat.event FROM game JOIN atbat ON game.game_id=atbat.game_id WHERE atbat.pitcher = %s AND game.date %s '%s' ORDER BY game.date DESC LIMIT %s'''

    params = (batter_id, operator, date.strftime("%Y-%m-%d"), abs(count))

    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, params)

    return_list = list(cur.fetchall())

    return return_list


def prepost_aggregate_opp_stats(inj_id, window):
    # Retrieve the injury details
    inj = injury.get_injury(inj_id)

    # Generate aggregate stats for window days before and after the injury
    stats = {
        "pre": batter.aggregate_stats(aggregatable_stats_window(inj["player_id_mlbam"], inj["start_date"], window*-1)),
        "post": batter.aggregate_stats(aggregatable_stats_window(inj["player_id_mlbam"], inj["end_date"], window))
    }

    return stats


def aggregatable_stats_window(pitcher_id, date, count):
    conn = connect.sqlalchemy_open()

    if count < 0:
        operator = "<"
    else:
        operator = ">="
    sql = "SELECT * FROM aggregate_batting WHERE pitcher = %s AND date %s '%s' ORDER BY game_id, inning, num LIMIT %s" \
          % (pitcher_id, operator, date.strftime("%Y-%m-%d"), abs(count))

    return pandas.read_sql_query(sql, conn)


def get_pitch_types(player_id, date, count):
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


def create_prepost_pitch_selection_histograms(injury_id, window):
    '''Create histograms of pitch selection before and after an injury'''

    max_window_size = injury.get_max_pitch_window(injury_id)
    if window > max_window_size:
        window = max_window_size

    inj = injury.get_injury(injury_id)
    pre = get_pitch_types(inj["player_id_mlbam"], inj["start_date"], window*-1)
    post = get_pitch_types(inj["player_id_mlbam"], inj["start_date"], window)

    print "pre:"
    for row in pre.iterrows():
        print row[1]["pitch_type"], "=", row[1]["pitch_count"]

    print "\npost:"
    for row in post.iterrows():
        print row[1]["pitch_type"], "=", row[1]["pitch_count"]


    graphics.create_bar_chart(pre, post, injury_id, window)
