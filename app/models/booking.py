from app import db
from models.users import User
from models.golf_courses import Golf_Courses

class Booking(db.Document):
    
    meta = {'collection': 'booking'}
    course = db.ReferenceField(Golf_Courses)
    user = db.ReferenceField(User)
    teetime = db.ListField()

    