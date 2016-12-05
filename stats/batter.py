from db import connect
from db import query
from injury import injury
import player
from datetime import datetime
import numpy
import pandas
import MySQLdb


def prepost_heatmap_coordinates(inj_id, window, result=""):

    inj_dates = injury.get_injury(inj_id)

    strt_dte = inj_dates['start_date']
    end_dte = inj_dates['end_date']
    plyr_id = inj_dates['player_id_mlbam']

    neg_window = window*(-1)


    pre_inj = get_pitches(plyr_id, strt_dte, neg_window)
    post_inj = get_pitches(plyr_id, end_dte, window)

    return pre_inj, post_inj


def get_pitches(batter_id, date, count, columns=(), result=""):
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
    params = (batter_id, date.strftime("%Y-%m-%d"), abs(count))

    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, params)

    return_list = list(cur.fetchall())

    return return_list


def get_atbats(batter_id, date, count, columns=()):

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
