from db import connect
from db import query
import MySQLdb
import pandas
import pitcher, batter, injury


def split_type(player_id):
    """Determines whether a player is, by default, a pitcher or a batter."""
    sql = '''
        SELECT type
        FROM gameday.player
        WHERE id = %s
    '''
    params = (player_id,)

    return query.select_single(sql, params)


def get_player(player_id):
    """Retrieve all information about a player, given their MLBAM id."""
    sql = '''
        SELECT *
        FROM gameday.player
        WHERE id = %s
    '''
    params = (player_id,)

    return query.select_first_row(sql, params)


def all_players_with_injuries(type="all", year=None):
    """Retrieve all players with at least one completed DL stint. Can be filtered by player type and year."""
    conn = connect.open()

    # If type is set, filter. Otherwise, get all players.
    if type in ["batter", "pitcher"]:
        type_condition = "AND type='%s'" % type
    else:
        type_condition = ""

    # If year is set, filter.
    if year:
        year_condition = "AND YEAR(start_date) = %s" % year
    else:
        year_condition = ""

    # Build and execute query
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
    """Given a pandas dataframe of plate appearance information, generate a standard array of aggregate stats."""
    if len(stats) > 0:
        # The basic stats are just totals of each possible outcome
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

        # Generate the core batting stats that can be derived from the above totals.
        agg["AVG"] = round(float(agg["1B"]+agg["2B"]+agg["3B"]+agg["HR"])/float(agg["AB"]), 3)
        agg["OBP"] = round(float(agg["1B"]+agg["2B"]+agg["3B"]+agg["HR"]+agg["BB"]+agg["IBB"]+agg["HBP"])/float(agg["PA"]), 3)
        agg["SLG"] = round(float(agg["1B"]+2*agg["2B"]+3*agg["3B"]+4*agg["HR"])/float(agg["AB"]), 3)
        agg["OPS"] = agg["OBP"] + agg["SLG"]

        return agg
    else:
        return None


def aggregatable_stats_window(player_id, date, count, player_type=""):
    """Retrieve a dataframe of individual plate appearances and their outcomes, for later aggregation."""
    conn = connect.sqlalchemy_open()

    # If the call does not specify batter or pitcher, determine that player's default type
    if not player_type:
        player_type = split_type(player_id)

    # If count is negative, get plate appearances prior to date. Otherwise, on or after.
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
    """Given a specific injury and a window, retrieve the aggregate stats
    for that window size before and after the injury."""

    # Retrieve the injury details
    inj = injury.get_injury(inj_id)

    # Generate aggregate stats for window events before and after the injury
    stats = {
        "pre": aggregate_stats(aggregatable_stats_window(inj["player_id_mlbam"], inj["start_date"], window*-1)),
        "post": aggregate_stats(aggregatable_stats_window(inj["player_id_mlbam"], inj["end_date"], window))
    }

    return stats


def slash_line(agg_stats):
    """Take the results of aggregate_stats and return a text formatted slash line (avg/obp/slg)"""
    return "/".join((format(agg_stats["AVG"], '.3f').lstrip("0"),
                     format(agg_stats["OBP"], '.3f').lstrip("0"),
                     format(agg_stats["SLG"], '.3f').lstrip("0")))


def get_pitches(player_id, date, count, columns=(), result="swing", player_type=""):
    """Retrieve all pitches over a given count for a player. This function calls out to the batter- and
    pitcher-specific versions of get_pitches."""
    if player_type not in ["pitcher", "batter"]:
        player_type = split_type(player_id)

    if player_type == "batter":
        return batter.get_pitches(player_id, date, count, columns, result)
    else:
        return pitcher.get_pitches(player_id, date, count, columns)
