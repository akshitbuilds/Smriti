import sqlite3
con = sqlite3.connect('smriti.db')
cur = con.cursor()
cur.execute('SELECT * FROM memories')
for row in cur.fetchall():
    print(row)
