from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, IntegerField, SelectField, DateTimeField, DateTimeLocalField
from wtforms.validators import InputRequired, Email, EqualTo, Regexp
from flask_wtf.file import FileField, FileRequired, FileAllowed

ALLOWED_FILE =['PNG','JPG','JPEG','png','jpg','jpeg'] 


class EventForm(FlaskForm):
  name = StringField('Event Name', validators=[InputRequired()])
  # adding two validators, one to ensure input is entered and other to check if the 
  #description meets the length requirements
  description = TextAreaField('Description', validators = [InputRequired()])
  eventImage = FileField('Event Poster/ Image', validators=[
    FileRequired(message = 'Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])
  ticketPrice = IntegerField('Ticket Price', validators = [InputRequired()])
  location = StringField('Event Address', validators=[InputRequired()])
  category = SelectField(u'Event Category', choices=[('local', 'Local'), ('imported', 'Imported'), ('emerging', 'Emerging'), ('impromptu', 'Impromptu')], validators=[InputRequired()])
  status = SelectField(u'Event Status', choices=[('open', 'Open'), ('inactive', 'Inactive'), ('sold out', 'Sold Out'), ('cancelled', 'Cancelled')], validators=[InputRequired()])
  eventTime = DateTimeField('Event Date & Time in YYYY-MM-DD HH:MM:SS', validators=[InputRequired()])
  #eventTime = DateTimeLocalField('Event Date & Time', format='%Y-%m-%dT%H:%M')
  venueName = StringField('Venue Name', validators=[InputRequired()])
  venueType = StringField('Venue Type', validators=[InputRequired()])
  ticketsAvailable = IntegerField('No. of Tickets Available', validators = [InputRequired()])
  submit = SubmitField("Create Event")

class EditForm(FlaskForm):
  name = StringField('Event Name', validators=[InputRequired()])
  # adding two validators, one to ensure input is entered and other to check if the 
  #description meets the length requirements
  description = TextAreaField('Description', validators = [InputRequired()])
  eventImage = FileField('Event Poster/ Image', validators=[
    FileRequired(message = 'Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])
  ticketPrice = IntegerField('Ticket Price', validators = [InputRequired()])
  location = StringField('Event Address', validators=[InputRequired()])
  category = SelectField(u'Event Category', choices=[('local', 'Local'), ('imported', 'Imported'), ('emerging', 'Emerging'), ('impromptu', 'Impromptu'), InputRequired()])
  eventTime = DateTimeField('Event Date & Time in YYYY-MM-DD HH:MM:SS', validators=[InputRequired()])
  venueName = StringField('Venue Name', validators=[InputRequired()])
  venueType = StringField('Venue Type', validators=[InputRequired()])
  ticketsAvailable = IntegerField('No. of Tickets Available', validators = [InputRequired()])
  submit = SubmitField("Update Event")




  
#User login
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")



#User register
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email"), InputRequired()])
    address = StringField("Address", validators=[InputRequired()])
    #contactNo = IntegerField('Contact No.', validators = [InputRequired()])
    contactNo = StringField( 'Phone Number', validators=[InputRequired(), Regexp(r'^(\d{10}|\d{2} \d{4} \d{4}|\d{4} \d{3} \d{3})$', message="Please enter a valid phone number.")])
    #linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    #submit button
    submit = SubmitField("Register")

#User comment
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Submit')
