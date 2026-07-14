from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(10), default='medium')  # low, medium, high
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Todo {self.id}: {self.title}>'

# Create database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    # Get filter parameter
    filter_type = request.args.get('filter', 'all')
    
    if filter_type == 'completed':
        todos = Todo.query.filter_by(completed=True).order_by(Todo.created_at.desc()).all()
    elif filter_type == 'active':
        todos = Todo.query.filter_by(completed=False).order_by(Todo.created_at.desc()).all()
    else:
        todos = Todo.query.order_by(Todo.created_at.desc()).all()
    
    # Statistics
    total_todos = Todo.query.count()
    completed_todos = Todo.query.filter_by(completed=True).count()
    active_todos = Todo.query.filter_by(completed=False).count()
    
    return render_template('index.html', 
                         todos=todos, 
                         filter_type=filter_type,
                         total_todos=total_todos,
                         completed_todos=completed_todos,
                         active_todos=active_todos)

@app.route('/add', methods=['POST'])
def add_todo():
    title = request.form.get('title')
    description = request.form.get('description')
    priority = request.form.get('priority', 'medium')
    
    if not title or title.strip() == '':
        flash('Title is required!', 'error')
        return redirect(url_for('index'))
    
    new_todo = Todo(
        title=title.strip(),
        description=description.strip() if description else None,
        priority=priority
    )
    
    try:
        db.session.add(new_todo)
        db.session.commit()
        flash('Todo added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error adding todo!', 'error')
    
    return redirect(url_for('index'))

@app.route('/complete/<int:id>')
def complete_todo(id):
    todo = Todo.query.get_or_404(id)
    todo.completed = not todo.completed
    
    try:
        db.session.commit()
        status = 'completed' if todo.completed else 'marked as active'
        flash(f'Todo {status} successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error updating todo!', 'error')
    
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    
    try:
        db.session.delete(todo)
        db.session.commit()
        flash('Todo deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting todo!', 'error')
    
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_todo(id):
    todo = Todo.query.get_or_404(id)
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority')
        
        if not title or title.strip() == '':
            flash('Title is required!', 'error')
            return render_template('edit.html', todo=todo)
        
        todo.title = title.strip()
        todo.description = description.strip() if description else None
        todo.priority = priority
        todo.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('Todo updated successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating todo!', 'error')
    
    return render_template('edit.html', todo=todo)

@app.route('/clear-completed')
def clear_completed():
    try:
        Todo.query.filter_by(completed=True).delete()
        db.session.commit()
        flash('All completed todos cleared!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error clearing completed todos!', 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)