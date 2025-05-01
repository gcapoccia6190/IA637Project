
# --- book.py ---
from baseObject import BaseObject

class Book(BaseObject):
    def __init__(self):
        table = 'Book'
        fields = ['BookID', 'Title', 'Author', 'ISBN', 'Genre', 'Status', 'EditionNumber', 'PublishYear']
        super().__init__(table, fields)
