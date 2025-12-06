from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Tag, Todo
from utils.email import send_reminder_email
from datetime import datetime
import os
import bcrypt

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-change-me')

# DATABASE CONFIG – CRITICAL FIX FOR psycopg3
db_url = os.environ.get('DATABASE_URL')

if db_url:
    # Force SQLAlchemy to use psycopg3 driver (not psycopg2!)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        'postgres://', 'postgresql+psycopg://', 1
    )
else:
    # Local dev fallback
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()
    # Seed sample tags if none exist
    if Tag.query.count() == 0:
        for t in [('Work', '#e74c3c'), ('Personal', '#3498db'), ('Urgent', '#f39c12')]:
            db.session.add(Tag(name=t[0], color=t[1]))
        db.session.commit()

@app.route('/')
@login_required
def index():
    q = request.args.get('q', '').strip()
    base = Todo.query.filter_by(user_id=current_user.id)
    if q:
        base = base.filter(Todo.text.ilike(f'%{q}%'))
    todos = base.order_by(Todo.complete.asc(), db.func.coalesce(Todo.due_date, '9999-12-31'), Todo.id.desc()).all()
    tags = Tag.query.all()
    return render_template('index.html', todos=todos, tags=tags)

@app.route('/add', methods=['POST'])
@login_required
def add():
    text = request.form['text'].strip()
    due_str = request.form.get('due_date')
    tag_ids = request.form.getlist('tags')
    
    due = datetime.strptime(due_str, '%Y-%m-%d').date() if due_str else None
    todo = Todo(text=text, due_date=due, user_id=current_user.id)
    db.session.add(todo)
    db.session.flush()  # Get ID for tags
    
    for tid in tag_ids:
        tag = Tag.query.get(tid)
        if tag:
            todo.tags.append(tag)
    
    db.session.commit()
    flash('Todo added!', 'success')
    return redirect(url_for('index'))

@app.route('/complete/<int:todo_id>')
@login_required
def complete(todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()
    if todo:
        todo.complete = True
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
@login_required
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    flash('Deleted!', 'success')
    return redirect(url_for('index'))

@app.route('/calendar')
@login_required
def calendar():
    todos = Todo.query.filter_by(user_id=current_user.id).all()
    events = []
    for t in todos:
        if t.due_date:
            events.append({
                'title': t.text[:50] + (' ✓' if t.complete else ''),
                'start': t.due_date.isoformat(),
                'color': '#27ae60' if t.complete else ('#e74c3c' if t.is_overdue() else '#3498db')
            })
    return render_template('calendar.html', events=events)

@app.route('/api/todos')
@login_required
def api_todos():
    # For FullCalendar
    todos = Todo.query.filter_by(user_id=current_user.id).all()
    events = []
    for t in todos:
        if t.due_date:
            events.append({
                'title': t.text,
                'start': t.due_date.isoformat(),
                'allDay': True
            })
    return jsonify(events)

# Auth routes (register, login, logout) – same as before, but add email to register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('Username or email taken!', 'error')
            return render_template('register.html')
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = User(username=username, email=email, password_hash=hashed)
        db.session.add(user)
        db.session.commit()
        flash('Registered! Log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and bcrypt.checkpw(request.form['password'].encode('utf-8'), user.password_hash.encode('utf-8')):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid login', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
