from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db  = SQLAlchemy(app)

class Event(db.Model):
    __tablename__ = 'Events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)
    lieu = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable = False)

    def __repr__(self):
        return f"Event('{self.title}', '{self.type}', '{self.date}', '{self.lieu}', '{self.description}')"
    
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__" :
    app.run(debug=True)
