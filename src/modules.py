"""Main project modules"""

from flask import request,session
from flask.wrappers import Request
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
import os,random

def genkey():
    """Generate random key"""
    key = Fernet.generate_key()
    return key.decode()

def Encrypt_Text():
    data = request.get_json()
    if not data["value"] == '':
        try:
            key = data["key"]
            value = data["value"]
            fernet = Fernet(key)
            plaintext = value.encode()
            encryptedtext = fernet.encrypt(plaintext)
            return {"status":"1","value":encryptedtext.decode()}
        except:
            return {"status":"0","value":"Encryption failed! , possible problem: key not found or invalid key"}
    else:
        return {"status":"0","value":"Encryption failed! , No text to encrypt, please type something"}

def Decrypt_Text():
    data = request.get_json()
    if not data["value"] == '':
        try:
            key = data["key"]
            value = data["value"]
            fernet = Fernet(key)
            plaintext = value.encode()
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

def Upload_file():
    """Upload the file from the client to ther server"""

    if not request.form["key"] == "":
        user_name = session.get('username','not set')
        cwd = os.getcwd()
        parent_dir = f'{cwd}/src/static/uploads' # set path
        path = os.path.join(parent_dir, user_name) # temporary folder with same name as guest username
        os.mkdir(path) #create temp dir
        
        uploaded_file = request.files["file"]
        uploaded_file.save(os.path.join(path,secure_filename(uploaded_file.filename))) # save file to the temp dir
        filename = secure_filename(uploaded_file.filename) # get filename
        session["path"]=path 
        session["filename"]=filename
    else:
        raise Exception("key not found") # no key specified - raise error - the file will be deleted.   
    
def Encrypt_file():
    """Encrypt uploaded file"""
    
    # get filename from path generated before
    path = session.get('path','not set')
    filename = session.get('filename','not set')
    
    key = request.form["key"]
    fernet = Fernet(key)
    with open(os.path.join(path,filename) , 'rb') as f:
        data = f.read()
    encryptedfile = fernet.encrypt(data)
    with open(os.path.join(path,filename),'wb') as f:
        f.write(encryptedfile)
    return filename

def Decrypt_file():
    """Decrypt uploaded file"""

    path = session.get('path','not set')
    filename = session.get('filename','not set')
    
    key = request.form["key"]
    fernet = Fernet(key)
    with open(os.path.join(path,filename) , 'rb') as f:
        data = f.read()
    decryptedfile = fernet.decrypt(data)
    with open(os.path.join(path,filename),'wb') as f:
        f.write(decryptedfile)
    return filename    


def SetupGuestSession():
    """Setup a guest session when an user enters the website, only for file upload"""
    
    import string
    user_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    session["username"] = user_name
    session["path"] = ""
    session["filename"] = ""  
