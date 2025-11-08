from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# ----------------------------------------------------
# Database Configuration (absolute path for reliability)
# ----------------------------------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, 'incidents.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ----------------------------------------------------
# Database Model
# ----------------------------------------------------
class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Incident {self.title}>"

# ----------------------------------------------------
# Initialize DB
# ----------------------------------------------------
with app.app_context():
    db.create_all()

# ----------------------------------------------------
# Routes
# ----------------------------------------------------
@app.route('/')
def index():
    incidents = Incident.query.order_by(Incident.created_at.desc()).all()
    return render_template('index.html', incidents=incidents)

@app.route('/add', methods=['POST'])
def add_incident():
    title = request.form['title']
    description = request.form['description']
    priority = request.form['priority']
    new_incident = Incident(title=title, description=description, priority=priority)
    db.session.add(new_incident)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>')
def update_incident(id):
    incident = Incident.query.get_or_404(id)
    incident.status = "Resolved" if incident.status == "Pending" else "Pending"
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_incident(id):
    incident = Incident.query.get_or_404(id)
    db.session.delete(incident)
    db.session.commit()
    return redirect(url_for('index'))

# ----------------------------------------------------
# Run Flask App
# ----------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
