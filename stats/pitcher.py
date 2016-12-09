from db import connect
import numpy
import pandas
import batter, graphics, injury
import MySQLdb


def heatmap_coordinates(inj_id, window):
    inj_dates = injury.get_injury(inj_id)

    strt_dte = inj_dates['start_date']
    end_dte = inj_dates['end_date']
    plyr_id = inj_dates['player_id_mlbam']

    neg_window = window*(-1)

    pre_inj = get_pitches(plyr_id, strt_dte, neg_window)
    post_inj = get_pitches(plyr_id, end_dte, window)

    return pre_inj, post_inj


def get_pitches(pitcher_id, date, count, columns=()):
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
    if count < 0:
        operator = "<"
    else:
        operator = ">="

    conn = connect.open()

    sql = '''
        SELECT g.date, ab.event
        FROM gameday.game g
            INNER JOIN gameday.atbat ab ON g.game_id=ab.game_id
        WHERE ab.pitcher = %s AND g.date __operator__ %s
        ORDER BY g.date DESC
        LIMIT %s
    '''
    sql = sql.replace("__operator__", operator)

    params = (pitcher_id, date.strftime("%Y-%m-%d"), abs(count))

    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, params)

    return_list = list(cur.fetchall())

    return return_list


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


def get_prepost_pitch_selection_histogram(injury_id, window):
    '''Create graph comparing of pitch selection before and after an injury'''

    inj = injury.get_injury(injury_id)

    pre = get_pitch_types(inj["player_id_mlbam"], inj["start_date"], window*-1)
    post = get_pitch_types(inj["player_id_mlbam"], inj["start_date"], window)
    return graphics.create_bar_chart(pre, post, window)

