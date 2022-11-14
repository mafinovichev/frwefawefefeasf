import sqlite3

conn = sqlite3.connect(r'data.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS status(
   tgid TEXT,
   status TEXT,
   current_word INT);
""")
conn.commit()