from datetime import datetime
from flask_login import UserMixin

from . import db

# class EnumCat(enum.Enum):
#     one = 'Local'
#     two = 'Imported'
#     three = 'Emerging'
#     four = 'Impromptu'

class User(db.Model, UserMixin):
    __tablename__ = 'users' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
	#password is never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)
    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user')
    # Define a many-to-many relationship for booked events
    bookings = db.relationship('Bookings', backref='user', lazy='dynamic')
    #backref events to user
    
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
    category = db.Column(db.String(400))
    status = db.Column(db.String(400))
    eventTime = db.Column(db.DateTime())
    venueName = db.Column(db.String(120))
    venueType = db.Column(db.String(120))
    ticketsAvailable = db.Column(db.Integer())
    # Define a many-to-many relationship for users who have booked this event
    bookings = db.relationship('Bookings', backref='event', lazy='dynamic')
    # ... Create the Comments db.relationship
	# relation to call destination.comments and comment.destination
    comments = db.relationship('Comment', backref='event')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
   
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
    

class Bookings(db.Model, UserMixin):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    num_tickets = db.Column(db.Integer, nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __init__(self, user_id, event_id, num_tickets):
        self.user_id = user_id
        self.event_id = event_id
        self.num_tickets = num_tickets