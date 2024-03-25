from flask import Blueprint, request, jsonify, render_template, session, send_file
from .models import db, User, ReportInfo
from flask_login import LoginManager, login_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from PyPDF2 import PdfReader, PdfWriter
import os

encrypt_file = Blueprint('encrypt_file', __name__)


@encrypt_file.route('/download', methods=['GET'])
def share_data():
    return render_template('download.html')


@encrypt_file.route('/verify-user', methods=['POST'])
@login_required
def verify_user():
    data = request.get_json()
    login_password = data['loginPassword']

    # verify user's login password
    user = User.query.get(current_user.id)
    if not check_password_hash(user.password_hash, login_password):
        return jsonify({'success': False, 'message': 'Invalid login password'}), 401

    return jsonify({'success': True, 'message': 'Login Verification successful'})


@encrypt_file.route('/encrypt-report', methods=['POST'])
@login_required
def encrypt_report():
    try:
        # Get user's  report password
        data = request.get_json()
        report_password = data['reportPassword']

        current_directory = os.path.dirname(os.path.abspath(__file__))

        file_path = os.path.join(current_directory, 'pdf-documents', 't224-fill-23e.pdf')

        print(file_path)

        # Encrypt the PDF report with user's login password
        encrypted_file_path = encrypt_pdf(file_path, report_password)

        # Store the path or identifier of the encrypted file
        # (in the user session, database, etc., depending on your application logic)
        store_encrypted_file_path(encrypted_file_path)
        return jsonify({'success': True})
    except Exception as e:
        # Log the error message for debugging
        print(str(e))
        # Return a JSON response with the error message
        response = jsonify({'success': False, 'message': 'Server error: ' + str(e)})
        response.status_code = 500
        return response


@encrypt_file.route('/download-report', methods=['GET'])
@login_required
def download_report():
    # Retrieve the stored path or identifier of the encrypted file
    encrypted_file_path = retrieve_encrypted_file_path()
    return send_file(encrypted_file_path, as_attachment=True)


'''''''FUNCTIONS'''''''


def encrypt_pdf(file_path, password):
    # Read the original PDF
    reader = PdfReader(file_path)
    writer = PdfWriter()

    # Copy all pages from the reader to the writer
    for page in reader.pages:
        writer.add_page(page)

    # Encrypt the new PDF
    writer.encrypt(password)

    # Save the encrypted PDF to a new file
    encrypted_file_path = file_path.replace(".pdf", "_encrypted.pdf")
    with open(encrypted_file_path, "wb") as encrypted_file:
        writer.write(encrypted_file)

    return encrypted_file_path




def store_encrypted_file_path(encrypted_file_path):
    # Store the encrypted file path in the user's session
    session['encrypted_file_path'] = encrypted_file_path


def retrieve_encrypted_file_path():
    # Retrieve the encrypted file path from the user's session
    return session.get('encrypted_file_path')
