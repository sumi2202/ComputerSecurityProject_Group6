from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)  # Student or Admin


class ReportInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Referencing the student id
    file_path = db.Column(db.String(255), nullable=False)  # Path to encrypted file
    document_type = db.Column(db.String(255), nullable=False)  # Financial Document or Tax Document
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, user_id, file_path, password):
        self.user_id = user_id
        self.file_path = file_path
        self.password_hash = generate_password_hash(password)

