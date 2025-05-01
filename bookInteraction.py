# --- bookInteraction.py ---
from baseObject import BaseObject

class BookInteraction(BaseObject):
    def __init__(self):
        table = 'BookInteraction'
        fields = ['InteractionID', 'UserID', 'BookID', 'InteractionType', 'Content', 'Rating', 'Event', 'Date', 'Time', 'Location']
        super().__init__(table, fields)

