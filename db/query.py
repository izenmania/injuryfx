from db import connect
import MySQLdb


def select_list(query):
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