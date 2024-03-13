from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes

# Function to generate the RSA keys
def generate_rsa_keys():
    key = RSA.generate(2048)        # Generates a pair of RSA keys that have a size of 2048 bits
    private_key = key.export_key()  # Exports the private key to string
    public_key = key.publickey().export_key()       # Exports the public key to string

    with open("uni_private_key.pem", "wb") as prv_file:  # Writes the pirvate key to a file
        prv_file.write(private_key)

    with open("uni_public_key.pem", "wb") as pub_file:   # Writes the public key to a file
        pub_file.write(public_key)
    pass

# Function to perform AES encryption for the uploaded files
def encrypt_aes(filename):

    # Generates the AES key, which is 16 random bytes
    aes_key = get_random_bytes(16)

    # Encrypt the file with AES
    aescipher = AES.new(aes_key, AES.MODE_EAX)      # Makes new AES cipher in EAX mode
    with open(filename, 'rb') as f:
        plaintext = f.read()                        # Reads the content in the file
    ciphertext, tag = aescipher.encrypt_and_digest(plaintext)     # Performs the encryption
    with open(filename, 'wb') as f:
        [f.write(x) for x in (aescipher.nonce, tag, ciphertext)]    # Writes the ciphertext, nonce, and tag to file

    # Use the public RSA key to encrypt the AES key
    receiver_key = RSA.import_key(open("uni_public_key.pem").read())
    rsacipher = PKCS1_OAEP.new(receiver_key)        # Creates RSA cipher
    encrypted_aes_key = rsacipher.encrypt(aes_key)        # Performs the encryption of the AES key

    # Stores the AES key that was encrypted
    with open(filename + '.key', 'wb') as f:
        f.write(encrypted_aes_key)

# Function to perform AES decryption
def decrypt_aes(filename):

    # Reads the AES key that was encrypted
    with open(filename + '.key', 'rb') as f:
        encrypted_aes_key = f.read()

    # Use the private RSA key to do the AES decryption
    private_key = RSA.import_key(open("uni_private_key.pem").read())
    rsacipher = PKCS1_OAEP.new(private_key)
    aes_key = rsacipher.decrypt(encrypted_aes_key)

    # Reads the encrypted file data
    with open(filename, 'rb') as f:
        nonce, tag, ciphertext = [f.read(x) for x in (16, 16, -1)]

    # With the AES key, decrypt the file data
    aescipher = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
    data = aescipher.decrypt_and_verify(ciphertext, tag)

    # Write and save the decrypted data in a file
    with open(filename, 'wb') as f:
        f.write(data)

# Function to perform RSA-AES encryption and decryption of payment
def encrypt_decrypt_payment(amount):

    # Generate an AES key of 16 random bytes
    aes_key = get_random_bytes(16)

    # Payment amount entered is encrypted with the AES key
    aescipher = AES.new(aes_key, AES.MODE_EAX)
    data_to_encrypt = 'PAYM'.encode('utf-8') + amount.encode('utf-8')
    ciphertext, tag = aescipher.encrypt_and_digest(data_to_encrypt)
    encrypted_data = aescipher.nonce + tag + ciphertext

    # Use the public RSA key to encrypt the AES key
    receiver_key = RSA.import_key(open("uni_public_key.pem").read())
    rsacipher = PKCS1_OAEP.new(receiver_key)
    encrypted_aes_key = rsacipher.encrypt(aes_key)

    # With the private RSA key, the AES key is decrypted
    private_key = RSA.import_key(open("uni_private_key.pem").read())
    rsacipher = PKCS1_OAEP.new(private_key)
    decrypted_aes_key = rsacipher.decrypt(encrypted_aes_key)

    # Decrypt the payment amount with the AES key
    aescipher = AES.new(decrypted_aes_key, AES.MODE_EAX, nonce=aescipher.nonce)
    decrypted_data = aescipher.decrypt_and_verify(ciphertext, tag)

    return encrypted_data, decrypted_data

