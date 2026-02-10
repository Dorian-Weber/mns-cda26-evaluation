from flask import Flask, flash, render_template, request, redirect, url_for
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
    date = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable = False)

    def __repr__(self):
        return f"Event('{self.title}', '{self.type}', '{self.date}', '{self.location}', '{self.description}')"
    
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/events", methods=["GET"])
def events():
    all_events = Event.query.all()
    return render_template("newEvent.html", events=all_events)

@app.route("/events", methods=["POST"])
def add_event():
    title = request.form['title']
    type = request.form['type']
    date = request.form['date']
    location = request.form['location']
    description = request.form['description']

    new_event = Event(title=title, type=type, date=date, location=location, description=description)
    db.session.add(new_event)
    db.session.commit()
    
    flash("L'évènement a été ajouté avec succès !", "success")

    return redirect(url_for('home'))

if __name__ == "__main__" :
    app.run(debug=True)
