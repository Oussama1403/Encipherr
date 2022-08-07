from js import document,console,alert
from cryptography.fernet import Fernet
alert("Offline mode")
def genkey(*a,**k):
    key = Fernet.generate_key()
    document.getElementById("key").value = key.decode() # output key

def encrypt_text(*a,**k):
    data = document.getElementById('text').value
    if not data == '':
        try:
            key = document.getElementById('key').value
            value = data
            fernet = Fernet(key)
            plaintext = value.encode()
            encryptedtext = fernet.encrypt(plaintext)
            document.getElementById("text").value = encryptedtext.decode()
        except:
            alert("Encryption failed! , possible problem: key not found or invalid key")
    else:
        alert("Encryption failed! , No text to encrypt, please type something")

def decrypt_text(*a,**k):
    data = document.getElementById('text').value
    if not data == '':
        try:
            key = document.getElementById('key').value
            value = data
            fernet = Fernet(key)
            plaintext = value.encode()
            decryptedtext = fernet.decrypt(plaintext)
            #decrypt one more if the text is still encrypted with the same key.
            document.getElementById("text").value = decryptedtext.decode()
        except:
            alert("Decryption failed! , possible problem: key not found or invalid key")
    else:
        alert("Decryption failed! , No text to decrypt, please type something")   