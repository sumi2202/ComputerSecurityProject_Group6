from website import create_app
from website.keygeneration import generate_rsa_keys
import os

app = create_app()

# Set the value of 'UPLOAD_FOLDER' to the /website/uploadedfiles directory (folder)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'website', 'uploadedfiles')
generate_rsa_keys()     # Calls function to generate the RSA keys
if __name__ == '__main__':
    app.run(debug=True)


