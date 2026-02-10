from datetime import datetime
from flask import Flask, flash, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

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
    title = request.form['title']
    type = request.form['type']
    str_date = request.form['date']
    location = request.form['location']
    description = request.form['description']

    date = datetime.strptime(str_date, '%Y-%m-%d').date()

    new_event = Event(title=title, type=type, date=date, location=location, description=description)
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
