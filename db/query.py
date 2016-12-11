"""Functions for certain commonly used SELECT queries"""
from db import connect
import MySQLdb


def select_list(query):
    """Generates a list from a single-column SELECT. If the query returns multiple columns,
    only the first will be returned"""
    conn = connect.open()

    out = []

    try:
        cur = conn.cursor()
        cur.execute(query)
        for row in cur:
            out.append(row[0])
    finally:
        conn.close()

    return out


def select_single(query, params=()):
    """Returns a the first column of the first row of a SELECT. Intended for single-value queries, such as
    retrieving a general body region based on a specific body part."""
    conn = connect.open()
    val = None

    try:
        cur = conn.cursor()
        cur.execute(query, params)
        if cur.rowcount > 0:
            val = cur.fetchone()[0]
    finally:
        conn.close()

    return val


def select_first_row(query, params=()):
    """Returns the entire first row of a SELECT result. Intended for single-row queries, such as
    retrieving a record based on primary key."""
    conn = connect.open()
    row = None

    try:
        cur = conn.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(query, params)
        if cur.rowcount > 0:
            row = cur.fetchone()
    finally:
        conn.close()

    return row