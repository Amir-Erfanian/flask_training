from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'Students'
    
    StudentID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Phone = db.Column(db.String(20))
    DateOfBirth = db.Column(db.Date)
    Course = db.Column(db.String(100))
    GPA = db.Column(db.Numeric(3, 2))
    EnrollmentDate = db.Column(db.DateTime, default=datetime.utcnow)
    IsActive = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Student {self.FirstName} {self.LastName}>'
    
    def to_dict(self):
        """Convert student object to dictionary for JSON responses"""
        return {
            'StudentID': self.StudentID,
            'FirstName': self.FirstName,
            'LastName': self.LastName,
            'Email': self.Email,
            'Phone': self.Phone,
            'DateOfBirth': self.DateOfBirth.strftime('%Y-%m-%d') if self.DateOfBirth else None,
            'Course': self.Course,
            'GPA': float(self.GPA) if self.GPA else None,
            'EnrollmentDate': self.EnrollmentDate.strftime('%Y-%m-%d %H:%M'),
            'IsActive': self.IsActive,
            'FullName': f"{self.FirstName} {self.LastName}"
        }
    
    @property
    def full_name(self):
        return f"{self.FirstName} {self.LastName}"