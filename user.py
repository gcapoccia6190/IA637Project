from baseObject import BaseObject
from flask_bcrypt import check_password_hash


class User(BaseObject):
    def __init__(self):
        table = 'User'
        fields = ['UserID', 'FullName', 'Username', 'PasswordHash', 'Email', 'Role']
        super().__init__(table, fields)

    @classmethod
    def verify_login(cls, username, password):
        temp = cls()
        temp.cur.execute("SELECT * FROM User WHERE Username = %s", (username,))
        user = temp.cur.fetchone()
        print("🔍 Raw DB user row:", user)
        return user  # just return here temporarily
