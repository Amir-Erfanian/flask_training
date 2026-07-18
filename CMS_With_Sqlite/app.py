from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    major = db.Column(db.String(100))
    
    def __repr__(self):
        return f'<Student {self.name}>'

@app.route("/")
def index():
    return redirect(url_for("students"))

from flask import request

@app.route("/students")
def students():

    search = request.args.get("search", "")
    major = request.args.get("major", "")

    query = Student.query

    if search:
        query = query.filter(Student.name.contains(search))

    if major:
        query = query.filter(Student.major == major)

    students = query.all()

    majors = db.session.query(Student.major).distinct().all()

    return render_template(
        "students.html",
        students=students,
        majors=majors,
        total=len(students),
        search=search,
        selected_major=major
    )

@app.route("/student/<int:id>")
def student(id):
    student = Student.query.get_or_404(id)
    return render_template("view_student.html", student=student)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    student = Student.query.get_or_404(id)
    if request.method == "POST":
        student.name = request.form.get("name")
        student.age = request.form.get("age")
        student.major = request.form.get("major")
        
        db.session.commit()
        return redirect(url_for("students"))
    
    return render_template("edit_student.html", student=student)

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for("students"))

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        major = request.form.get("major")
        
        if age:
            age = int(age)
        else:
            age = 0
        
        student = Student(name=name, age=age, major=major)
        db.session.add(student)
        db.session.commit()
        
        return redirect(url_for("students"))
    
    return render_template("add_student.html")

with app.app_context():
    db.create_all()
    print("Database tables created successfully!")

if __name__ == '__main__':
    app.run(debug=True)