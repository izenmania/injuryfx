import re

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
            "injury": results.group(7).replace(".", ""),
        }
    else:
        fields = {}

    return(fields)


def parse_injury(inj):
    pass

def parse_injury_transaction(raw_injury):
    global __directions, __dl_types, __injury_terms, __positions

    # search_string = raw_injury["team"] + \
    #                 " (" + '|'.join(__injury_terms) + ")" + \
    #                 " (" + '|'.join(__positions) + ") " + \
    #                 raw_injury["player"] + \
    #                 " (" + '|'.join(__directions) + ")" + \
    #                 " the( 15-day disabled list to the)?" + \
    #                 " (" + '|'.join(__dl_types) + ")" + \
    #                 " disabled list( .*)?\. ?(.*)?"
    # results = re.search(search_string, raw_injury["note"])

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