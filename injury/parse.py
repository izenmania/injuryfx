import re
from db import query

# note = trans["note"]
# team = trans["team"]
# player = trans["player"]
#
# searchString = team+" ("+'|'.join(injuryTerms)+") ("+'|'.join(positions)+") "+player+" ("+'|'.join(directions)+") the (.*) list\."
# results = re.search(searchString, note)

__injury_terms = ["activated", "placed", "transferred"]
__positions = ["C", "1B", "2B", "3B", "SS", "RF", "CF", "LF", "OF", "DH", "RHP", "LHP"]
__directions = ["from", "on", "to"]
__dl_types = ["15-day", "60-day"]

__part_key_list = query.select_list("SELECT exact FROM body_part_map")


# Take the note string from an injury transaction and extract fields
def parse_note(note, team_name, player_name):

    search_string = team_name + \
                    " (" + '|'.join(__injury_terms) + ")" + \
                    " (" + '|'.join(__positions) + ") " + \
                    player_name + \
                    " (" + '|'.join(__directions) + ")" + \
                    " the( 15-day disabled list to the)?" + \
                    " (" + '|'.join(__dl_types) + ")" + \
                    " disabled list( .*)?\. ?(.*)?"

    results = re.search(search_string, note)

    if results:
        fields = {
            "action": results.group(1),
            "dl_type": results.group(5),
        }

        inj = parse_injury(results.group(7).replace(".", ""))
        fields.update(inj)
    else:
        fields = {}

    return fields


# Take the injury field parsed out of the note string and extract fields
def parse_injury(inj):
    global __part_key_list
    injury = {}
    if inj:
        inj = inj.lower()
        injury["injury"] = inj
        # Extract side
        if "left" in inj:
            injury["side"] = "left"
        elif "right" in inj:
            injury["side"] = "right"
        else:
            injury["side"] = ""

        # Extract and translate body part
        # Get list of body part words from database. TEMP VERSION:

        parts = list(set([get_general_part(p) for p in __part_key_list if p in inj]))
        injury["parts"] = parts
        # TODO: if body part isn't found, then later process is needed to hunt for entries with an injury but no part

    return injury


def parse_injury_transaction(raw_injury):
    global __directions, __dl_types, __injury_terms, __positions

    note = parse_note(raw_injury["note"], raw_injury["team"], raw_injury["player"])

    inj = {
        "transaction_id": raw_injury["player"],
        "transaction_date": raw_injury["effective_date"],
        "player_name": raw_injury["player"],
        "player_id_mlbam": raw_injury["player_id"],
        "team_name": raw_injury["team"],
        "team_id_mlbam": raw_injury["team_id"],
        "note": raw_injury["note"]
    }
    inj.update(note)

    return (inj)


# Return a general body part from the exact part
def get_general_part(exact):
    return query.select_single("SELECT general FROM body_part_map WHERE exact = %s", (exact))