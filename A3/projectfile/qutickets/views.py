from flask import Blueprint, render_template, request
from .models import Event, Comment
from . import db


main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods= ["GET", "POST"])
def index():
    events = db.session.query(Event).all()
    
    if request.method == 'POST':
            search = request.form["searchBar"]
            tag = "%{}%".format(search)
            events = db.session.query(Event).filter(Event.name.like(tag)).all()

    return render_template('index.html', events=events)