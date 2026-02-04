import sqlite3

connection = sqlite3.connect("testdb.db")
cursor = connection.cursor()

# create a table
cursor.execute("""CREATE TABLE IF NOT EXISTS shipment
                (id INTEGER,
                content TEXT,
                weight REAL,
                status TEXT)
                """)

# insert a row
cursor.execute("""INSERT INTO shipment
                VALUES (12701, 'computer', 12.8, 'in-transit')
                """)

cursor.execute("""SELECT * FROM shipment
                """)

row = cursor.fetchall()
print(row)

connection.commit()


connection.close()