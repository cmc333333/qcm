import sqlite3

conn = sqlite3.connect('qcm.db')

conn.execute("""
    CREATE TABLE IF NOT EXISTS activities (
      key INTEGER PRIMARY KEY AUTOINCREMENT,
      value TEXT  --  JSON
    );
    """)
conn.execute("""
    CREATE TABLE IF NOT EXISTS metric (
      key INTEGER PRIMARY KEY AUTOINCREMENT,
      value TEXT  --  JSON
    );
    """)
conn.commit()
