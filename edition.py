# --- edition.py ---
from baseObject import BaseObject

class Edition(BaseObject):
    def __init__(self):
        table = 'Edition'
        fields = ['EditionID', 'BookID', 'EditionNumber', 'PublishYear', 'Format']
        super().__init__(table, fields)
