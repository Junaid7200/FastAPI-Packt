import sqlite3
from typing import Any
from schemas import Shipment, ShipmentUpdateModel
from contextlib import contextmanager



class Database():
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
    def connect_to_db(self):
            self.conn = sqlite3.connect("shipmentdb.db", check_same_thread=False)
            self.cursor = self.conn.cursor()
    def close(self):
        self.conn.close()

    # def __enter__(self):
    #     print("enter the context")
    #     self.connect_to_db()
    #     self.create_table()
    #     return self
    # def __exit__(self, *arg):
    #     print("exiting the context")
    #     self.close()

@contextmanager
def managed_db():
    db = Database()
    db.connect_to_db()
    db.create_table()
    try:
        yield db
    finally:
        db.close()

with managed_db() as db:
    print(db.get(1))










# old practice

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