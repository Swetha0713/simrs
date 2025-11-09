from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from functools import wraps
import os

# ----------------------------------------------------
# App setup
# ----------------------------------------------------
app = Flask(__name__)
app.secret_key = 'simrs-secret-key'  # in production, use .env

bcrypt = Bcrypt(app)

# ----------------------------------------------------
# Database configuration
# ----------------------------------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, 'incidents.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ----------------------------------------------------
# Database models
# ----------------------------------------------------
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

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
# Initialize DB and seed admin
# ----------------------------------------------------
with app.app_context():
    db.create_all()
    if not Admin.query.filter_by(username="admin").first():
        hashed_pw = bcrypt.generate_password_hash("admin123").decode('utf-8')
        db.session.add(Admin(username="admin", password=hashed_pw))
        db.session.commit()

# ----------------------------------------------------
# Helper: Login required decorator
# ----------------------------------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please login first', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ----------------------------------------------------
# Authentication routes
# ----------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()

        if admin and bcrypt.check_password_hash(admin.password, password):
            session['admin_id'] = admin.id
            session['admin_name'] = admin.username
            flash('Login successful', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

# ----------------------------------------------------
# Main routes (protected)
# ----------------------------------------------------
@app.route('/')
@login_required
def index():
    search = request.args.get('search', '')
    if search:
        incidents = Incident.query.filter(
            (Incident.title.ilike(f'%{search}%')) |
            (Incident.priority.ilike(f'%{search}%'))
        ).order_by(Incident.created_at.desc()).all()
    else:
        incidents = Incident.query.order_by(Incident.created_at.desc()).all()
    return render_template('index.html', incidents=incidents)

@app.route('/add', methods=['POST'])
@login_required
def add_incident():
    title = request.form['title']
    description = request.form['description']
    priority = request.form['priority']
    new_incident = Incident(title=title, description=description, priority=priority)
    db.session.add(new_incident)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>')
@login_required
def update_incident(id):
    incident = Incident.query.get_or_404(id)
    incident.status = "Resolved" if incident.status == "Pending" else "Pending"
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
@login_required
def delete_incident(id):
    incident = Incident.query.get_or_404(id)
    db.session.delete(incident)
    db.session.commit()
    return redirect(url_for('index'))

# ----------------------------------------------------
# API endpoints (for testing)
# ----------------------------------------------------
@app.route('/api/incidents', methods=['GET'])
def api_get_all():
    incidents = Incident.query.order_by(Incident.created_at.desc()).all()
    return jsonify([{
        "id": i.id,
        "title": i.title,
        "description": i.description,
        "priority": i.priority,
        "status": i.status,
        "created_at": i.created_at.isoformat()
    } for i in incidents])

@app.route('/api/incidents', methods=['POST'])
def api_add_incident():
    data = request.get_json()
    new = Incident(
        title=data.get("title"),
        description=data.get("description"),
        priority=data.get("priority", "Low")
    )
    db.session.add(new)
    db.session.commit()
    return jsonify({"message": "Incident added successfully"}), 201

# ----------------------------------------------------
# Run
# ----------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
