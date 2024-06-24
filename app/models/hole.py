from app import db

class Hole(db.EmbeddedDocument):
 
    meta = {'collection': 'hole'}
    index = db.IntField()
    par = db.IntField()
    dist = db.IntField()