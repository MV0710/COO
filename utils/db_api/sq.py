import sqlite3
connection = sqlite3.connect('a.db',check_same_thread=False)
cursor = connection.cursor()
connection.commit()
connection.close()