from datetime import datetime
from flask import Flask, flash, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel, Field, constr
import datetime as dt

app = Flask(__name__)
secret_key = "my_secret_key"

app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db  = SQLAlchemy(app)

class Event(db.Model):
    __tablename__ = 'Events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable = False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"Event('{self.title}', '{self.type}', '{self.date}', '{self.location}', '{self.description}','{self.date_created}')"

class CreateEvent(BaseModel):
    title: constr(strip_whitespace=True, min_length=1, max_length=50) # type: ignore
    type: constr(strip_whitespace=True, min_length=1, max_length=50) # type: ignore
    date: dt.date
    location: constr(strip_whitespace=True, min_length=1, max_length=50) # type: ignore
    description: constr(strip_whitespace=True, min_length=1, max_length=100) # type: ignore

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    all_events = Event.query.all()
    return render_template("home.html", events=all_events)

@app.route("/events", methods=["GET"])
def events():
    all_events = Event.query.all()
    return render_template("newEvent.html", events=all_events)

@app.route("/events", methods=["POST"])
def add_event():
    data = request.form.to_dict()

    required_fields = ["title", "type", "date", "location", "description"]

    if any(not data.get(field) 
           for field in required_fields):
        flash("Tous les champs sont obligatoires !", "error")
        return redirect(url_for('events'))
    try:
        validated: CreateEvent = CreateEvent.model_validate(data)
    except Exception as e:
        flash(f"Tous les champs sont obligatoires !", "error")
        return redirect(url_for('events'))

    new_event = Event(**validated.model_dump())
    db.session.add(new_event)
    db.session.commit()
    
    flash("L'évènement a été ajouté avec succès !", "success")
    return redirect(url_for('home'))

@app.route("/delete-envents/<int:id>")
def delete_event(id):
    entry = Event.query.get(id)
    if not entry :
        flash("Entrée d'historique non trouvée", "error")
        return redirect(url_for("home"))
    db.session.delete(entry)
    db.session.commit()
    flash("Entrée d'historique supprimée avec succès", "success")
    return  redirect(url_for("home"))


@app.route("/events/upcoming", methods=["GET"])
def get_upcoming_events():
    events = (
        db.session.query(Event)
        .filter(Event.date >= datetime.today())
        .order_by(Event.date.asc())
        .limit(5)
        .all()
    )
    return jsonify([{
        "id": event.id,
        "title": event.title,
        "type": event.type,
        "date": event.date,
        "location": event.location,
        "description": event.description
    } for event in events])


if __name__ == "__main__" :
    app.run(debug=True)
