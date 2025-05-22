import sqlite3

# Establish a connection and a cursor
connection = sqlite3.connect("data.db")
cursor = connection.cursor()

# Query all data on a condition
cursor.execute("SELECT * FROM events WHERE date='2024.09.03'")
rows =cursor.fetchall()
print(rows)

# Query certian columns
cursor.execute("SELECT band, date FROM events WHERE date='2024.07.02'")
rows =cursor.fetchall()
print(rows)

# # Insert new rows
# new_rows = [('Cat', 'Cat City', '2024.10.17'),
#             ('Hens', 'Hen City', '2024.11.17')]
#
# cursor.executemany("INSERT INTO events VALUES(?, ?,?)", new_rows)
# connection.commit()

cursor.execute("SELECT * FROM events")
rows =cursor.fetchall()
print(rows)