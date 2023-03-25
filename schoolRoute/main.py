import psycopg2

try:
    conn = psycopg2.connect(
        database="schoolroute",
        user="gerente",
        password="Gerente123498765",
        host="localhost",
        port="5432"
    )

    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()

    for row in rows:
        print(row)
finally:
    cur.close()
    conn.close()