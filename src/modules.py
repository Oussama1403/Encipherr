"""Main project modules"""

from flask import request,session
from flask.wrappers import Request
from werkzeug.utils import secure_filename
from .app import app
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os,random

class TextEncryption():
    
    def __init__(self):
        data = request.get_json() 
        self.key = Utils.return_key(data["key"],data["key_type"])
        self.value = data["value"]
    
    def encrypt(self):
        """Encrypt Text"""

        if not self.value == '':
            try:
                fernet = Fernet(self.key)
                plaintext = self.value.encode()
                encryptedtext = fernet.encrypt(plaintext)
                return {"status":"1","value":encryptedtext.decode()}
            except:
                return {"status":"0","value":"Encryption failed! , possible problem: key not found or invalid key"}
        else:
            return {"status":"0","value":"Encryption failed! , No text to encrypt, please type something"}
    
    def decrypt(self):
        """Decrypt Text"""

        if not self.value == '':
           try:
               fernet = Fernet(self.key)
               plaintext = self.value.encode()
               decryptedtext = fernet.decrypt(plaintext)
               # Decrypt text until get an unencrypted text ( useful when the text is encrypted multiple times )
               while True:
                   try:
                       decryptedtext = fernet.decrypt(decryptedtext)
                   except:
                       return {"status":"1","value":decryptedtext.decode()}
           except:
               return {"status":"0","value":"Decryption failed! , possible problem: key not found or invalid key"}
        else:
            return {"status":"0","value":"Decryption failed! , No text to decrypt, please type something"}       

class FileEncryption():
    
    def __init__(self):
        data = request.form 
        self.key = Utils.return_key(data["key"],data["key_type"])
        self.path = session.get('path','not set')
        self.filename = session.get('filename','not set')
    
    def encrypt(self):
        """Encrypt uploaded file"""

        fernet = Fernet(self.key)
        with open(os.path.join(self.path,self.filename) , 'rb') as f:
            data = f.read()
        encryptedfile = fernet.encrypt(data)
        with open(os.path.join(self.path,self.filename),'wb') as f:
            f.write(encryptedfile)
        return self.filename

    def decrypt(self):
        """Decrypt uploaded file"""
        
        #key = request.form["key"]
        fernet = Fernet(self.key)
        with open(os.path.join(self.path,self.filename) , 'rb') as f:
            data = f.read()
        decryptedfile = fernet.decrypt(data)
        with open(os.path.join(self.path,self.filename),'wb') as f:
            f.write(decryptedfile)
        return self.filename    


class Utils():
    
    def return_key(key,type):
        """generate key from custom pwd if key_type == pwd else return the AES key"""

        if type == "pwd":
            if key == "":return ""
            salt = app.config["SALT"]
            kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,)
            key = base64.urlsafe_b64encode(kdf.derive(key.encode()))
            return key
        else:
            return key    
    
    def genkey():
        """Generate random key"""
        key = Fernet.generate_key()
        return key.decode()
    
    def SetupGuestSession():
        """Setup a guest session when an user enters the website, only for file upload"""
        
        import string
        user_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        session["username"] = user_name
        session["path"] = ""
        session["filename"] = ""
    
    def Upload_file():
        """Upload the file from the client to ther server"""
    
        if not request.form["key"] == "":
            user_name = session.get('username','not set')
            parent_dir = app.config["UPLOAD_FOLDER"] # set path
            path = os.path.join(parent_dir, user_name) # temporary folder with same name as guest username
            os.mkdir(path) #create temp dir
            
            uploaded_file = request.files["file"]
            uploaded_file.save(os.path.join(path,secure_filename(uploaded_file.filename))) # save file to the temp dir
            filename = secure_filename(uploaded_file.filename) # get filename
            session["path"]=path 
            session["filename"]=filename
        else:
            raise Exception("key not found") # no key specified - raise error - the file will be deleted.          




