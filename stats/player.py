from db import connect
from db import query
import MySQLdb

# Determines if a player's most useful splits are pitching or batting
def split_type(player_id):
    sql = '''
        SELECT
            IF(SUM(pitcher = %s) > SUM(batter = %s), "pitcher", "batter")
        FROM gameday.pitch
        WHERE pitcher = %s OR batter = %s
    '''
    params = (player_id, player_id, player_id, player_id)
    return query.select_single(sql, params)


def get_player(player_id):
    sql = '''
        SELECT *
        FROM gameday.player
        WHERE id = %s
    '''
    params = (player_id,)

    return query.select_first_row(sql, params)


def all_players_with_injuries(type="all", year=None):
    conn = connect.open()

    if type in ["batter", "pitcher"]:
        type_condition = "AND type='%s'" % type
    else:
        type_condition = ""

    if year:
        year_condition = "AND YEAR(start_date) = %s" % year
    else:
        year_condition = ""

    sql = '''
        SELECT p.id, p.first_name, p.last_name, p.type, COUNT(*) AS injury_count, MAX(i.start_date) AS latest_injury
        FROM injuryfx.injuries i
            INNER JOIN gameday.player p ON p.id = i.player_id_mlbam
        WHERE i.end_date IS NOT NULL
            %s
            %s
        GROUP BY p.id
        ORDER BY p.last_name, p.first_name
    ''' % (type_condition, year_condition)

    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql)

    list = []
    for row in cur:
        list.append(row)

    return list
