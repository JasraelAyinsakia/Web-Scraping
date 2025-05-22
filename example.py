import sqlite3

# Establish a connection and a cursor
connection = sqlite3.connect("data.db")
cursor = connection.cursor()

# Query all data
cursor.execute("SELECT * FROM events WHERE data='2024.09.03'")
rows =cursor.fetchall()
print(rows)
# Query certian columns
cursor.execute("SELECT band, date FROM events WHERE data='2024.07.02'")
rows =cursor.fetchall()
print(rows)

