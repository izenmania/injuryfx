"""Functions to process statistics specific to batters"""
from db import connect
from db import query
import player, injury
from datetime import datetime
import numpy
import pandas
import MySQLdb


def get_pitches(batter_id, date, count, columns=(), result="swing"):
    """Retrieve a given number (count) of pitches, before or after a given date, thrown to a batter.
    Can be filtered on batter action/pitch result."""

    # If count is negative, find pitches prior to the date. If positive, on or after the date.
    if count < 0:
        operator = "<"
    else:
        operator = ">="

    conn = connect.open()

    # Filter based on the desired outcome of the pitch
    if result == "swing":
        # All pitches swung at by the batter
        result_condition = "AND p.des NOT IN ('Called Strike', 'Ball')"
    elif result == "contact":
        # All pitches contacted by the batter
        result_condition = "AND p.des NOT IN ('Called Strike', 'Ball', 'Swinging Strike')"
    elif result == "play":
        # All pitches put into play
        result_condition = "AND p.des LIKE 'In play%'"
    elif result == "miss":
        # All pitches actively swung at and missed
        result_condition = "AND p.des = 'Swinging Strike'"
    else:
        result_condition = ""

    # Built and execute the query to retrieve pitch list
    sql = '''
        SELECT p.px AS x, p.pz AS y
        FROM gameday.game g
            INNER JOIN  gameday.pitch p ON g.game_id=p.game_id
        WHERE p.batter = %s AND g.date __operator__ %s
            __result_condition__
        ORDER BY g.date ASC
        LIMIT %s
    '''
    sql = sql.replace("__operator__", operator).replace("__result_condition__", result_condition)
    params = (batter_id, date.strftime("%Y-%m-%d"), abs(count))

    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, params)

    return_list = list(cur.fetchall())

    return return_list


def get_atbats(batter_id, date, count, columns=()):
    """Retrieve a given number (count) of at bats, before or after a given date, by a batter."""

    # If count is negative, find at-bats prior to the date. If positive, on or after the date.
    if count < 0:
        operator = "<"
    else:
        operator = ">="

    conn = connect.open()

    # Build and execute the query
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
