from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, session
from werkzeug.utils import secure_filename
from flask import current_app as app
import os
from .keygeneration import encrypt_aes, encrypt_decrypt_payment
from .keygeneration import decrypt_aes

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

#route for dashboard/profile page
@views.route('/profile_page')
def profile():
    return render_template("profile_page.html")

# Route for upload page
@views.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:         # Checks if file has been included with request or redirects user
            return redirect(request.url)

        file = request.files['file']           # Gets file and checks if a filename has been given or redirects
        if file.filename == '':
            flash('No file has been selected')
            return redirect(request.url)
        if file:                                # If file was uploaded
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # The file path (folder) that it uploads to
            file.save(file_path)
            encrypt_aes(file_path)  # Calls the encrypt_aes function to perform RSA-AES encryption from keygeneration.py

            session['uploaded_file'] = filename

            return redirect(url_for('views.uploaded_files'))
    return render_template("upload.html")

# Route for the uploaded_files page
@views.route('/uploaded_files')
def uploaded_files():
    filename = session.get('uploaded_file')  # From the session, gets the filename
    return render_template("uploaded_files.html", filename=filename)

# To download file from the uploaded_files page
@views.route('/uploadedfiles/<filename>')
def download_file(filename):
    decrypt_aes(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Calls the decrypt_aes function in keygeneration
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)   # Gets it from the specified directory

# Route for payment page
@views.route('/payment')
def payment():
    return render_template("payment.html")

# Route for submitted payment
@views.route('/submit_payment', methods=['POST'])
def submit_payment():
    amount = request.form.get('amount')     # Form to get the amount
    encrypted_data, decrypted_data = encrypt_decrypt_payment(amount)       # Calls the encrypt_decrypt_payment function
    return """
    <html>
    <body>
    <script>
    alert('Payment of $' + {} + ' received!');
    </script>
    </body>
    </html>
    """.format(decrypted_data.decode('utf-8')[4:])
