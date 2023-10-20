from . import db
from datetime import datetime
import enum
from sqlalchemy import Integer, Enum


# class EnumCat(enum.Enum):
#     one = 'Local'
#     two = 'Imported'
#     three = 'Emerging'
#     four = 'Impromptu'



class User(db.Model):
    __tablename__ = 'users' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
	# password should never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long, depending on your hashing algorithm
    password_hash = db.Column(db.String(255), nullable=False)
    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user')
    
    # string print method
    def __repr__(self):
        return f"Name: {self.name}"

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    eventImage = db.Column(db.String(400))
    ticketPrice = db.Column(db.Float())
    location = db.Column(db.String(120))
    # category = db.Column(db.Enum(EnumCat))
    category = db.Column(db.String(400))
    eventTime = db.Column(db.DateTime())
    venueName = db.Column(db.String(120))
    venueType = db.Column(db.String(120))
    ticketsAvailable = db.Column(db.Integer())

    
    # ... Create the Comments db.relationship
	# relation to call destination.comments and comment.destination
    comments = db.relationship('Comment', backref='event')
	
    # string print method
    def __repr__(self):
        return f"Name: {self.name}"

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    # add the foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    # string print method
    def __repr__(self):
        return f"Comment: {self.text}"