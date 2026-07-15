from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app
from models import db, Student
from datetime import datetime

# ============ READ - Display all students ============
@app.route('/')
def index():
    students = Student.query.filter_by(IsActive=True).order_by(Student.StudentID.desc()).all()
    return render_template('index.html', students=students)

# ============ CREATE - Add new student ============
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        try:
            # Get form data
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            dob = request.form.get('dob')
            course = request.form.get('course')
            gpa = request.form.get('gpa')
            
            # Validate required fields
            if not all([first_name, last_name, email]):
                flash('First Name, Last Name, and Email are required!', 'danger')
                return render_template('add_student.html')
            
            # Check if email already exists
            existing_student = Student.query.filter_by(Email=email).first()
            if existing_student:
                flash('Email already exists! Please use a different email.', 'danger')
                return render_template('add_student.html')
            
            # Create new student
            new_student = Student(
                FirstName=first_name,
                LastName=last_name,
                Email=email,
                Phone=phone,
                DateOfBirth=datetime.strptime(dob, '%Y-%m-%d') if dob else None,
                Course=course,
                GPA=float(gpa) if gpa else None
            )
            
            db.session.add(new_student)
            db.session.commit()
            
            flash(f'Student {first_name} {last_name} added successfully!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding student: {str(e)}', 'danger')
            return render_template('add_student.html')
    
    return render_template('add_student.html')

# ============ READ - View single student ============
@app.route('/student/<int:id>')
def view_student(id):
    student = Student.query.get_or_404(id)
    return render_template('view_student.html', student=student)

# ============ UPDATE - Edit student ============
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Update fields
            student.FirstName = request.form.get('first_name')
            student.LastName = request.form.get('last_name')
            student.Email = request.form.get('email')
            student.Phone = request.form.get('phone')
            dob = request.form.get('dob')
            student.DateOfBirth = datetime.strptime(dob, '%Y-%m-%d') if dob else None
            student.Course = request.form.get('course')
            gpa = request.form.get('gpa')
            student.GPA = float(gpa) if gpa else None
            student.IsActive = request.form.get('is_active') == 'on'
            
            db.session.commit()
            flash('Student updated successfully!', 'success')
            return redirect(url_for('view_student', id=student.StudentID))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating student: {str(e)}', 'danger')
    
    return render_template('edit_student.html', student=student)

# ============ DELETE - Soft delete ============
@app.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    try:
        # Soft delete (just deactivate)
        student.IsActive = False
        db.session.commit()
        flash(f'Student {student.full_name} deactivated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting student: {str(e)}', 'danger')
    
    return redirect(url_for('index'))

# ============ HARD DELETE - Permanently remove ============
@app.route('/delete/permanent/<int:id>', methods=['POST'])
def permanent_delete(id):
    student = Student.query.get_or_404(id)
    try:
        db.session.delete(student)
        db.session.commit()
        flash(f'Student {student.full_name} permanently deleted!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting student: {str(e)}', 'danger')
    
    return redirect(url_for('index'))

# ============ RESTful API endpoints ============
@app.route('/api/students', methods=['GET'])
def api_get_students():
    students = Student.query.filter_by(IsActive=True).all()
    return jsonify([student.to_dict() for student in students])

@app.route('/api/students/<int:id>', methods=['GET'])
def api_get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify(student.to_dict())

@app.route('/api/students', methods=['POST'])
def api_create_student():
    data = request.get_json()
    
    # Validate required fields
    if not all([data.get('FirstName'), data.get('LastName'), data.get('Email')]):
        return jsonify({'error': 'FirstName, LastName, and Email are required'}), 400
    
    # Check if email exists
    if Student.query.filter_by(Email=data['Email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    new_student = Student(
        FirstName=data['FirstName'],
        LastName=data['LastName'],
        Email=data['Email'],
        Phone=data.get('Phone'),
        Course=data.get('Course'),
        GPA=data.get('GPA')
    )
    
    db.session.add(new_student)
    db.session.commit()
    
    return jsonify(new_student.to_dict()), 201

# ============ Search functionality ============
@app.route('/search')
def search_students():
    query = request.args.get('q', '')
    if query:
        students = Student.query.filter(
            (Student.FirstName.contains(query)) | 
            (Student.LastName.contains(query)) | 
            (Student.Email.contains(query)) |
            (Student.Course.contains(query))
        ).filter_by(IsActive=True).all()
    else:
        students = Student.query.filter_by(IsActive=True).all()
    
    return render_template('index.html', students=students, search_query=query)