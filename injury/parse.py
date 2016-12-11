"""Functions for transforming raw JSON from the MLB transaction API into usable injury updates"""
import re
from db import query
from datetime import datetime

# Lists to facilitate note parsing.
__injury_terms = ["activated", "placed", "transferred"]
__positions = ["C", "1B", "2B", "3B", "SS", "RF", "CF", "LF", "OF", "DH", "RHP", "LHP"]
__directions = ["from", "on", "to"]
__dl_types = ["15-day", "60-day", "7-day"]
__part_key_list = query.select_list("SELECT exact FROM body_part_map")


def parse_note(note, team_name, player_name):
    """Take the note string from an injury transaction and extract various fields"""

    # Build and run a regular expression using other fields, and the term lists
    search_string = team_name + \
                    " ?(" + '|'.join(__injury_terms) + ")?" + \
                    " (" + '|'.join(__positions) + ") " + \
                    player_name + \
                    " (" + '|'.join(__directions) + ")" + \
                    " the( 15-day disabled list to the)?" + \
                    " (" + '|'.join(__dl_types) + ")" + \
                    " disabled list" + \
                    "( retroactive to [a-zA-Z]* \d{1,2}, \d{4})?\. ?"+\
                    "(.*)?"

    results = re.search(search_string, note)

    if results:
        # If the regex matched, extract fields
        fields = {
            "action": results.group(1),
            "dl_type": results.group(5),
        }

        # Sometimes the word "activated" is missing, but can be inferred.
        if not fields["action"]:
            if "from the 15-day" in note or "from the 60-day" in note:
                fields["action"] = "activated"

        # Extract the phrase describing the nature of the injury, and send it to parse_injury for additional details.
        inj = parse_injury(results.group(7).replace(".", ""))

        # Append the parsed injury information
        fields.update(inj)
    elif "activated" in note:
        # If the regex fails to match, but the word "activated" is present, set the action. Other fields are not needed.
        fields = {"action": "activated"}
    else:
        fields = {}

    return fields


def parse_injury(inj):
    """Take the injury text parsed out of the note string and extract details."""
    global __part_key_list
    injury = {}
    if inj:
        inj = inj.lower()
        injury["injury"] = inj

        # If side information is present, set side
        if "left" in inj:
            injury["side"] = "left"
        elif "right" in inj:
            injury["side"] = "right"
        else:
            injury["side"] = ""

        # Compare the text to the list of keywords stored in the body_part_map table to determine body region
        parts = list(set([get_general_part(p) for p in __part_key_list if p in inj]))
        injury["parts"] = parts

    return injury


def parse_injury_transaction(raw_injury):
    """Take the raw JSON from the MLB transaction API and convert to a saveable dict."""

    # Send the note field, which contains most of the detail, to be parsed.
    note = parse_note(raw_injury["note"], raw_injury["team"], raw_injury["player"])

    # Get the useful additional fields from the JSON, converting type where needed.
    inj = {
        "transaction_id": raw_injury["transaction_id"],
        "transaction_date": datetime.strptime(raw_injury["effective_date"], "%Y-%m-%dT%H:%M:%S"),
        "player_name": raw_injury["player"],
        "player_id_mlbam": raw_injury["player_id"],
        "team_name": raw_injury["team"],
        "team_id_mlbam": raw_injury["team_id"],
        "note": raw_injury["note"]
    }
    # Incorporate the parsed note information.
    inj.update(note)

    return (inj)


def get_general_part(exact):
    """Return a general body area based on a specific body part keyword."""
    return query.select_single("SELECT general FROM body_part_map WHERE exact = %s", (exact,))
