from db import connect
from db import query

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