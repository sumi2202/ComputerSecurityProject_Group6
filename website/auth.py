from flask import Blueprint, render_template, jsonify, request
from flask_login import login_user
from werkzeug.security import check_password_hash
from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET'])
def login():
    return render_template("login.html")
@auth.route('/login', methods=['POST'])
def authenticate_login(authenticated=None):
    data = request.get_json()
    student_id = data['student_id']
    password = data['password']

    # Authenticate the user
    user = User.query.filter_by(student_id=student_id).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401


@auth.route('/logout')
def logout():
    return "<p>Logout</p>"


@auth.route('/sign-up')
def sign_up():
    return render_template("signup.html")
