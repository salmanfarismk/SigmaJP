import sqlite3
conn = sqlite3.connect('sigmajp.db')
conn.execute('DELETE FROM cards')
conn.commit()
conn.close()
print("Cleared")