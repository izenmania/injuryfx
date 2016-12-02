from db import connect
from injury import injury

# These functions are a lot like those in pitcher, but pull events based on the batter rather than pitcher
# Additionally, some of the functions include a "result" field.
# This is intended to let us get only pitches that the batter swings at, or only those that he makes contact with, etc.


def heatmap_coordinates(inj_id, window, result=""):
    # TODO: Provide a list of two sets of coordinates to be passed to graphics.generate_heatmap
    # window is the number of pitches in each direction to retrieve
    # Use injury.load_injury(inj_id, (player_id_mlbam, start_date, end_date)) to get details
    # Use two calls to get_pitches with the player id,  dates from load_injury, and the window value (one positive, one negative)
    pass


def get_pitches(batter_id, date, count, columns=(), result=""):
    # TODO: return a list of pitch events starting from a certain date
    # If count is negative, return that many before the date. Otherwise, after (including the date itself).
    # If columns is empty, return all columns from the pitch table. Otherwise, only those specified.
    pass


def get_atbats(batter_id, date, count, columns=()):
    # TODO: return a list of atbat events starting from a certain date
    # If count is negative, return that many before the date. Otherwise, after (including the date itself).
    # If columns is empty, return all columns from the atbat table. Otherwise, only those specified.
    pass