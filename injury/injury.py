import sys
from db import connect
from db import query
import json
from datetime import datetime
import exceptions


# save_injury: Take a dict from parse_injury_transaction save it in the database
# This function is intended to be run chronologically over the entries in the json files.
# Transfer and activate options rely on finding the most recent prior transaction for the player.
def save_injury(inj):
    out = ""
    conn = connect.open()

    try:
        cur = conn.cursor()

        if inj['action'] == "placed":
            # This is a new injury, so insert it fresh.
            insert_sql = '''
                INSERT INTO injuries (
                    injury_id, player_id_mlbam, team_id_mlbam, injury, side, parts, dl_type, start_date, end_date
                ) VALUES (
                    null, %s, %s, %s, %s, %s, %s, %s, NULL
                )
            '''
            params = (
                inj['player_id_mlbam'],
                inj['team_id_mlbam'],
                inj['injury'] if 'injury' in inj else '',
                inj['side'] if 'side' in inj else '',
                json.dumps(inj['parts']) if 'parts' in inj else '',
                inj['dl_type'],
                inj['transaction_date'].strftime("%Y-%m-%d")
            )

            out = cur.execute(insert_sql, params)
            conn.commit()

        else:
            # Get the most recent uncompleted injury by the player
            select_sql = '''
                SELECT injury_id
                FROM injuries
                WHERE player_id_mlbam = %s
                    AND end_date IS NULL
                ORDER BY start_date DESC
                LIMIT 1
            '''
            inj_id = query.select_single(select_sql, (inj['player_id_mlbam'],))

            if inj_id:
                if inj['action'] == 'activated':
                    # The injury incident is over, set the end_date
                    update_sql = '''
                        UPDATE injuries
                        SET end_date = %s
                        WHERE injury_id = %s
                    '''
                    params = (
                        inj['transaction_date'].strftime("%Y-%m-%d"),
                        inj_id
                    )

                    out = cur.execute(update_sql, params)
                    conn.commit()
                else:
                    # The player has moved from 15-day to 60-day DL, update dl_type
                    update_sql = '''
                        UPDATE injuries
                        SET dl_type = %s
                        WHERE injury_id = %s
                    '''

                    params = (
                        inj['dl_type'],
                        inj_id
                    )

                    out = cur.execute(update_sql, params)
                    conn.commit()
            else:
                # No matching injury entry was found.
                out = "Error: no injury match found."
                # TODO: log the unmatched injury to somewhere

    # TODO: improve error handling
    except exceptions.TypeError as e:
        print(e)
    except exceptions.AttributeError as e:
        print(e)
    except:
        print("Error!", sys.exc_info()[0])

    return out


# Load the details of a single injury by id
def get_injury(inj_id, columns=""):
    # TODO: retrieve a single injury row from the database based on injury_id.
    # If columns is empty, return all. Otherwise, only those specified.

    conn = connect.open()

    # (13330L, 452095L, 144L, 'fractured left hand', 'left', '["hand"]', '15-day', datetime.date(2016, 7, 10), datetime.date(2016, 8, 17))

    sql = '''
        SELECT injury_id, player_id_mlbam, team_id_mlbam, injury, side, parts, dl_type, start_date, end_date
        FROM injuries
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
            "parts": json.loads(res[5]),
            "dl_type": res[6],
            "start_date": res[7],
            "end_date": res[8]
        }

        return inj
    else:
        return None



# Find all injuries matching the given set of search terms
def search_injuries(name="", start_date="", end_date=""):
    pass