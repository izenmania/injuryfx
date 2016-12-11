"""Functions for saving parsed injuries to the database for later analysis"""
import sys
from db import connect
from db import query
import json
from datetime import date
import exceptions


# save_injury: Take a dict from parse_injury_transaction save it in the database
# This function is intended to be run chronologically over the entries in the json files.
# Transfer and activate options rely on finding the most recent prior transaction for the player.
def save_injury(inj):
    """Takes a parsed injury dict, as returned by parse.parse_injury_transaction, and saves it to the database.
    This function is intended to be run chronologically over the entries in the MLB.com JSON files, as transfer
    and activate actions rely on finding the most recent prior transaction for the player."""
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
            # This is an activation or a transfer to the 60-day DL, which means it is an update to an existing row.
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
                # TODO: log the unmatched injury to somewhere, for later review.

    except exceptions.TypeError as e:
        print(e)
    except exceptions.AttributeError as e:
        print(e)
    except:
        print("Error!", sys.exc_info()[0])

    return out


def log_save(transaction_id, transaction_date):
    """Logs the latest save point of the transaction import, so that the process can pick up where it left off."""
    conn = connect.open()
    sql = "INSERT INTO injury_load_log VALUES (NULL, %s, %s, CURRENT_TIMESTAMP)"
    params = (transaction_id, transaction_date.strftime("%Y-%m-%d"))
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()


def next_month(d):
    """Take any date object and return a date object of the first day of the next month."""
    y = d.year
    m = d.month
    new_m = d.month + 1
    new_y = y
    if new_m > 12:
        new_m = 1
        new_y += 1
    return date(new_y, new_m, 1)