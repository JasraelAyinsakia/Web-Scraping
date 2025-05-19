import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM events WHERE band='Lion'")
rows =cursor.fetchall()
print(rows)