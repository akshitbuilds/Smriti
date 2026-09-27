import sqlite3
con = sqlite3.connect('smriti.db')
cur = con.cursor()
for t in ['messages','memories','actions','audit_log']:
    cur.execute(f'SELECT COUNT(*) FROM {t}')
    print(t, cur.fetchone())
