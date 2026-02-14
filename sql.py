import sqlite3
from typing import Any
from schemas import Shipment, ShipmentUpdateModel



class Database():
    def __init__(self):
        self.conn = sqlite3.connect("shipmentdb.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()
    def create_table(self):
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS shipment
                            (id INTEGER PRIMARY KEY,
                            content TEXT,
                            weight REAL,
                            status TEXT
                            )""")
    def create(self, shipment: Shipment) -> int:
        self.cursor.execute("""
                    SELECT MAX(id) FROM shipment """)
        result = self.cursor.fetchone()
        new_id = (result[0] or 0) + 1
        self.cursor.execute("""
                            INSERT INTO shipment
                            VALUES (:id, :content, :weight, :status)""", {
                                "id": new_id,
                                **shipment.model_dump()
                            })
        self.conn.commit()
        return new_id

    def get(self, id: int) -> dict[str, Any] | None:
        self.cursor.execute("""
                            SELECT * FROM shipment WHERE id = ?""", (id, ))
        result = self.cursor.fetchone()
        if result is None:
            return None
        return {
            "id": result[0],
            "content": result[1],
            "weight": result[2],
            "status": result[3]
        }
    def update(self, id: int, shipment: ShipmentUpdateModel):
        self.cursor.execute("""
                            UPDATE shipment SET status = :status WHERE id = :id """, {
                                "status": shipment.status,
                                "id": id
                            })
        self.conn .commit()
        return self.get(id)
    def delete(self, id: int):
        self.cursor.execute("""
                            DELETE FROM shipment WHERE id = ?""", (id,))
        self.conn.commit()
        return self.cursor.rowcount > 0
    def close(self):
        self.conn.close()
        


# # create a table
# cursor.execute("""CREATE TABLE IF NOT EXISTS shipment
#                 (id INTEGER PRIMARY KEY,
#                 content TEXT,
#                 weight REAL,
#                 status TEXT)
#                 """)

# INSERT A ROW
# cursor.execute("""INSERT INTO shipment
#                 VALUES (12701, 'computer', 12.8, 'in-transit')
#                 """)

# FETCH AND PRINT ROWS
# cursor.execute("""SELECT * FROM shipment
#                 """)
# row = cursor.fetchall()
# print(row)

# DELETE ROW
# cursor.execute("""DELETE FROM shipment WHERE id = 12701""")

# DELETE TABLE
# cursor.execute("""DROP TABLE shipment""")

# UPDATE A CELL
# cursor.execute("""UPDATE shipment SET status='completed' WHERE id=12701""")

# connection.commit()


# connection.close()