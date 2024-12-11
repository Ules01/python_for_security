from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# Define constants
AES_KEY = b'0123456789abcdef'
AES_IV  = b'0123456789abcdef' 


def _encrypt_body(email_body):
    if isinstance(email_body, str):
        try:
            email_body = email_body.encode('utf-8')
        except Exception as e:
            pass

    encryption_suite = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    padded_body = pad(email_body, AES.block_size)

    cipher_text = encryption_suite.encrypt(padded_body)

    return base64.b64encode(cipher_text).decode('utf-8')

def decrypt_body(encrypted_body):
    encrypted_body_bytes = base64.b64decode(encrypted_body)
    
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    
    decrypted_padded_body = cipher.decrypt(encrypted_body_bytes)
    decrypted_body = unpad(decrypted_padded_body, AES.block_size)
    
    return decrypted_body.decode('utf-8')