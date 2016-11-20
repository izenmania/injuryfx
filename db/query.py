from db import connect


def select_list(query):
    conn = connect.open()

    out = []

    try:
        with conn.cursor() as cur:
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
        with conn.cursor() as cur:
            cur.execute(query, params)
            if cur.rowcount > 0:
                val = cur.fetchone()[0]
    finally:
        conn.close()

    return val