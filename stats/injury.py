import sys
from db import connect
from db import query
import json
from datetime import datetime
import exceptions
import MySQLdb
import player


# Load the details of a single injury by id
def get_injury(inj_id, columns=""):

    conn = connect.open()

    sql = '''
        SELECT i.injury_id, i.player_id_mlbam, i.team_id_mlbam,
            i.injury, i.side, i.parts, i.dl_type,
            i.start_date, i.end_date,
            p.first_name, p.last_name
        FROM injuryfx.injuries i
            INNER JOIN gameday.player p ON p.id = i.player_id_mlbam
        WHERE injury_id = %s
    '''

    params = (inj_id,)
    cur = conn.cursor()
    cur.execute(sql, params)

    if cur.rowcount > 0:
        res = cur.fetchone()

        inj = {
            "injury_id": res[0],
            "player_id_mlbam": res[1],
            "team_id_mlbam": res[2],
            "injury": res[3],
            "side": res[4],
            "parts": json.loads(res[5]) if res[5] else "",
            "dl_type": res[6],
            "start_date": res[7],
            "end_date": res[8],
            "first_name": res[9],
            "last_name": res[10]
        }
        return inj
    else:
        return None



# Find all injuries matching the given set of search terms
def search_injuries(name="", start_date="", end_date=""):
    pass

# Find all injuries for a given player
def get_player_injuries(player_id):
    conn = connect.open()

    sql = '''
        SELECT i.injury_id, i.player_id_mlbam, i.team_id_mlbam,
            i.injury, i.side, i.parts, i.dl_type,
            i.start_date, i.end_date,
            p.first_name, p.last_name
        FROM injuryfx.injuries i
            INNER JOIN gameday.player p ON p.id = i.player_id_mlbam
        WHERE i.player_id_mlbam = %s
		AND i.end_date IS NOT NULL
        ORDER BY i.start_date DESC
    '''
    params = (player_id, )

    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, params)

    list = []
    for row in cur:
        row['parts'] = json.loads(row['parts']) if row['parts'] else ""
        list.append(row)

    return list

def _get_window_boundaries(injury_id, break_on_off_season=False):
    'Calculate max date boundaries around an injury.'

    conn = connect.open()

    # Get all injuries for a player based on the current injury_id
    # TODO there are instances where the end_date is null on an injury
    # They can cause weird results (such as the max window size being zero)
    # Code should handle these more elegantly.
    injuries_for_this_player_sql = '''
    select i2.injury_id, i1.player_id_mlbam, replace(i2.start_date, '-', '/') start_date, 
           i2.dl_type
    from injuryfx.injuries i1
         INNER JOIN injuryfx.injuries i2 ON i1.player_id_mlbam = i2.player_id_mlbam
    where i1.injury_id = %s
    order by i2.start_date
    '''

    params = (injury_id,)
    cur = conn.cursor()
    cur.execute(injuries_for_this_player_sql, params)

    injuries = []
    for res in cur.fetchall():
        injury = {
            "injury_id": res[0],
            "player_id_mlbam": res[1],
            "start_date": res[2],
            "dl_type": res[3],
        }
        injuries.append(injury)

    # determine injury date as well as prior and next injury date if they exist
    # otherwise set boundaries outside of the data time frames
    boundaries = { "prior_injury_date" : '0000/00/00',
                   "next_injury_date" : '9999/99/99',
                   "current_injury" : None }

    for i, injury in enumerate(injuries):
        if injury["injury_id"] == injury_id:
            if i > 0:
                boundaries["prior_injury_date"] = injuries[i-1]["start_date"]
            if i < len(injuries) - 1:
                boundaries["next_injury_date"] = injuries[i+1]["start_date"]
            boundaries["current_injury"] = injury
            break

    return boundaries

def get_max_atbat_window(injury_id, player_type=None, break_on_off_season=False):
    '''Calculate the maximum window size on each side of an injury for a batter.
    The borders are either defined as another injury or the break in a season
    if break_on_off_season == TRUE (TODO, make season break actually happen)
    '''

    boundaries = _get_window_boundaries(injury_id, break_on_off_season)
    
    current_injury_date = boundaries["current_injury"]["start_date"]
    player_id = boundaries["current_injury"]["player_id_mlbam"]

    if player_type is None:
       player_type = player.split_type(player_id)

    conn = connect.open()
    # get total number of events before injury and with lower boundary
    prior_sql = '''
    select count(*) total_prior_at_bats
    from gameday.atbat
    where _player_type_ = %s
    and substring(game_id, 1, 10) <= %s
    and substring(game_id, 1, 10) >= %s
    order by game_id, event_num;
    '''
    prior_sql = prior_sql.replace("_player_type_", player_type)

    params = (player_id, current_injury_date, boundaries["prior_injury_date"])
    cur = conn.cursor()
    cur.execute(prior_sql, params)

    prior_count = cur.fetchone()[0]

    # get total number of events after injury and with upper boundary
    post_sql = '''
    select count(*) total_prior_at_bats
    from gameday.atbat
    where _player_type_ = %s
    and substring(game_id, 1, 10) > %s
    and substring(game_id, 1, 10) < %s
    order by game_id, event_num;
    '''

    post_sql = post_sql.replace("_player_type_", player_type)

    params = (player_id, current_injury_date, boundaries["next_injury_date"])
    cur = conn.cursor()
    cur.execute(post_sql, params)

    post_count = cur.fetchone()[0]
    
    # return the smaller of these as the maximum window size
    max_window = min([post_count, prior_count])

    return max_window


def get_max_pitch_window(injury_id, player_type=None, break_on_off_season=False):
    '''Calculate the maximum window size on each side of an injury for a pitcher.
    The borders are either defined as another injury or the break in a season
    iif break_on_off_season == TRUE (TODO, make season break actually happen)
    '''
    boundaries = _get_window_boundaries(injury_id, break_on_off_season)

    current_injury_date = boundaries["current_injury"]["start_date"]
    player_id = boundaries["current_injury"]["player_id_mlbam"]

    if player_type is None:
       player_type = player.split_type(player_id)    


    conn = connect.open()
    # get total number of events before injury and with lower boundary
    prior_sql = '''
    select count(*) total_prior_pitches
    from gameday.pitch
    where _player_type_ = %s
    and substring(game_id, 1, 10) <= %s
    and substring(game_id, 1, 10) >= %s
    '''
    prior_sql = prior_sql.replace("_player_type_", player_type)

    params = (player_id, current_injury_date, boundaries["prior_injury_date"])
    cur = conn.cursor()
    cur.execute(prior_sql, params)

    prior_count = cur.fetchone()[0]

    # get total number of events after injury and with upper boundary
    post_sql = '''
    select count(*) total_prior_pitches
    from gameday.pitch
    where _player_type_ = %s
    and substring(game_id, 1, 10) > %s
    and substring(game_id, 1, 10) < %s
    '''

    post_sql = post_sql.replace("_player_type_", player_type)

    params = (player_id, current_injury_date, boundaries["next_injury_date"])
    cur = conn.cursor()
    cur.execute(post_sql, params)

    post_count = cur.fetchone()[0]
    
    # return the smaller of these as the maximum window size
    max_window = min([post_count, prior_count])

    return max_window


