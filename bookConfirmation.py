# --- bookConfirmation.py ---
from baseObject import BaseObject

from baseObject import BaseObject

class BookConfirmation(BaseObject):
    def __init__(self):
        table = 'BookConfirmation'
        fields = ['ConfirmationID', 'BookID', 'UserID', 'ConfirmationDate', 'Notes']
        super().__init__(table, fields)

