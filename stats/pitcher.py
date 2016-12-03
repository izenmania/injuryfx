from db import connect
from injury import injury
import numpy
import pandas
import batter

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