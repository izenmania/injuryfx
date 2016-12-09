from db import connect
from db import query
import MySQLdb
import pandas
import pitcher, batter, injury

# Determines if a player's most useful splits are pitching or batting
def split_type(player_id):
    sql = '''
        SELECT type
        FROM gameday.player
        WHERE id = %s
    '''
    params = (player_id,)

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


def aggregate_stats(stats):
    if len(stats) > 0:
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
    else:
        return None


def aggregatable_stats_window(player_id, date, count, player_type=""):
    conn = connect.sqlalchemy_open()

    if not player_type:
        player_type = split_type(player_id)

    if count < 0:
        operator = "<"
    else:
        operator = ">="

    sql = '''
        SELECT *
        FROM aggregate_batting
        WHERE __type__ = %s AND
            date __operator__ '%s'
        ORDER BY game_id, inning, num
        LIMIT %s
    ''' % (player_id, date, abs(count))

    sql = sql.replace("__type__", player_type).replace("__operator__", operator)

    return pandas.read_sql_query(sql, conn)


def prepost_aggregate_stats(inj_id, window):
    # Retrieve the injury details
    inj = injury.get_injury(inj_id)

    # Generate aggregate stats for window days before and after the injury
    stats = {
        "pre": aggregate_stats(aggregatable_stats_window(inj["player_id_mlbam"], inj["start_date"], window*-1)),
        "post": aggregate_stats(aggregatable_stats_window(inj["player_id_mlbam"], inj["end_date"], window))
    }

    return stats


# Take a the results of aggregate_stats and return a slash line (avg/obp/slg) in text format
def slash_line(agg_stats):
    return "/".join((format(agg_stats["AVG"], '.3f').lstrip("0"),
                     format(agg_stats["OBP"], '.3f').lstrip("0"),
                     format(agg_stats["SLG"], '.3f').lstrip("0")))


def get_pitches(player_id, date, count, columns=(), result="swing", player_type=""):
    if player_type not in ["pitcher", "batter"]:
        player_type = split_type(player_id)

    if player_type == "batter":
        return batter.get_pitches(player_id, date, count, columns, result)
    else:
        return pitcher.get_pitches(player_id, date, count, columns)
