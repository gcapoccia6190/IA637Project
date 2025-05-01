# --- baseObject.py ---
import pymysql

class BaseObject:
    def __init__(self, table, fields):
        self.table = table
        self.fields = fields
        self.conn = pymysql.connect(
            host='mysql.clarksonmsda.org',
            port=3306,
            user='ia637',
            passwd='ia637clarkson',
            db='ia637_capoccgmPROJECT',
            autocommit=True
        )
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)

    def select_all(self):
        self.cur.execute(f"SELECT * FROM {self.table}")
        return self.cur.fetchall()
    
    def select_where(self, condition):
        query = f"SELECT * FROM {self.table} WHERE {condition}"
        self.cur.execute(query)
        return self.cur.fetchall()


    def select_by_id(self, record_id, id_field):
        self.cur.execute(f"SELECT * FROM {self.table} WHERE {id_field} = %s", (record_id,))
        return self.cur.fetchone()

    def insert(self, values):
        fields_str = ", ".join(self.fields[1:])  # skip ID field
        placeholders = ", ".join(["%s"] * len(values))
        self.cur.execute(
            f"INSERT INTO {self.table} ({fields_str}) VALUES ({placeholders})",
            values
        )

    def delete_by_id(self, record_id, id_field):
        self.cur.execute(f"DELETE FROM {self.table} WHERE {id_field} = %s", (record_id,))

    def update_by_id(self, record_id, values, id_field):
        set_clause = ", ".join([f"{field} = %s" for field in self.fields[1:]])
        self.cur.execute(
            f"UPDATE {self.table} SET {set_clause} WHERE {id_field} = %s",
            values + [record_id]
        )


