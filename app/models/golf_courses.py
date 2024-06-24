from app import db
from models.hole import Hole

class Golf_Courses(db.Document):
 
    meta = {'collection': 'golf_courses'}
    course = db.StringField()
    img_url = db.StringField()
    description = db.StringField()
    holes = db.EmbeddedDocumentListField(Hole)
 