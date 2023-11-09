from flask import Blueprint, flash, render_template, request, redirect, url_for
from .models import Event, Comment, User
from .forms import EventForm, CommentForm, EditForm
from . import db
import os
from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from . import db
from .forms import CommentForm, EventForm
from .models import Bookings, Comment, Event

eventbp = Blueprint('event', __name__, url_prefix='/events')
current_time = datetime.now()


@eventbp.route('/')
def index():
    events = db.session.query(Event).all()
    return render_template('index.html', events=events)

@eventbp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    # create the comment form
    cform = CommentForm()    
    return render_template('events/showevent.html', event=event, form=cform)

@eventbp.route('/createevent', methods=['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = EventForm()
  if form.validate_on_submit():
    #call the function that checks and returns image
    db_file_path = check_upload_file(form)
    event = Event(name=form.name.data,description=form.description.data, 
    eventImage = db_file_path,ticketPrice=form.ticketPrice.data,
    location=form.location.data, category=form.category.data, status=form.status.data, 
    eventTime=form.eventTime.data, venueType=form.venueType.data, venueName=form.venueName.data,
    ticketsAvailable=form.ticketsAvailable.data, user_id=current_user.id)
    # add the object to the db session
    db.session.add(event)
    # commit to the database
    db.session.commit()
    print('Successfully created new event', 'success')
    flash('Succesfully created event')
    #Always end with redirect when form is valid
    return redirect(url_for('event.create'))
  return render_template('events/createEvent.html', form=form)


@eventbp.route('/<id>/edit', methods=['GET', 'POST'])
def editEvent(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    
    eform = EditForm(obj=event)
    if eform.validate_on_submit():
    #call the function that checks and returns image
        db_file_path = check_upload_file(eform)
        event.name=eform.name.data
        event.description=eform.description.data 
        event.eventImage = db_file_path 
        event.ticketPrice=eform.ticketPrice.data
        event.location=eform.location.data
        event.category=eform.category.data 
        event.eventTime=eform.eventTime.data
        event.venueType=eform.venueType.data
        event.venueName=eform.venueName.data
        event.ticketsAvailable=eform.ticketsAvailable.data
        #entry = event.query.get_or_404()
        
        db.session.commit()
        print('Successfully updated event', 'success')
        flash('Succesfully updated event')
    return render_template('events/edit.html', event=event, form=eform)
    



@eventbp.route('/<id>/cancel', methods=['GET', 'POST'])
def cancelEvent(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if(event.status != 'cancelled'):
        event.status = 'cancelled'
        db.session.commit()
        print('Successfully updated event', 'success')
        flash('Succesfully updated event')
    else:
        print('Event has already been cancelled', 'success')
        flash('Event is already cancelled')
    #return render_template('events/edit.html', event=event, form=eform)
    return redirect(url_for('event.show', id=id))
    
# def eventTimeOut():
#     current_time = datetime.now()
#     events = db.session.query(Event).all()

#     for event in events:
#         if event.eventTime < current_time and event.status not in ('cancelled', 'Sold Out'):
#             event.status = 'inactive'
#             db.session.commit()



def check_upload_file(form):
   #get file data from form
   fp = form.eventImage.data
   filename = fp.filename
   #get current path of the module file
   BASE_PATH = os.path.dirname(__file__)
   #Upload file location - dir of this file/static/image
   upload_path = os.path.join(BASE_PATH, 'static/img/', secure_filename(filename)) 
   #store relative path in db as img loc in html is relative
   db_upload_path = 'static/img/' + secure_filename(filename)
   #save the file and return the db upload path
   fp.save(upload_path)
   return db_upload_path


@eventbp.route('/<id>/comment', methods=['GET', 'POST'])  
@login_required
def comment(id):  
    form = CommentForm()  
    #get the destination object associated to the page and the comment
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if form.validate_on_submit():  
      # read the comment from the form, associate the Comment's destination field
      # with the destination object from the above DB query
      comment = Comment(text=form.text.data, event=event) 
      #here the back-referencing works - comment.destination is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 
      #flashing a message which needs to be handled by the html
      #flash('Your comment has been added', 'success')  
      print('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('event.show', id=id))

@eventbp.route('/<id>/purchase', methods=['POST'])
@login_required
def purchase(id):
    event = db.session.query(Event).get(id)
    num_tickets = int(request.form['ticketselect'])

    # Check if there are enough tickets available
    if num_tickets > event.ticketsAvailable:
        flash('Not enough seats available', 'danger')
        return redirect(url_for('event.show', id=id))

    # Process the purchase logic here
    # Update the database to reflect the purchased tickets and charge the user.

    ticket_purchase = Bookings(user_id=current_user.id, event_id=event.id, num_tickets=num_tickets)

    # Update the number of available tickets for the event
    event.ticketsAvailable -= num_tickets

    # Commit the changes to the database
    db.session.add(ticket_purchase)
    db.session.commit()

    flash('Tickets purchased successfully', 'success')

    return redirect(url_for('event.show', id=id))





@eventbp.route('/profile')
@login_required
def profile():
    
    #try:
    user_booked_events = current_user.bookings.all()
    #except AttributeError:
        #user_booked_events = []

    #print("User Booked Events:", user_booked_events)

    return render_template('profilePage.html', user=current_user, booked_events=user_booked_events)

