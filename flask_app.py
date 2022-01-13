#! /usr/bin/python3.9

from flask import Flask,flash,request,render_template,url_for,redirect,send_from_directory,abort,after_this_request,session,Response,stream_with_context
from flask.wrappers import Request
from werkzeug.utils import secure_filename
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from cryptography.fernet import Fernet
import os,random,shutil

app = Flask(__name__)
secret_key = os.urandom(24)
app.secret_key = secret_key

app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config['SESSION_TYPE'] = 'sqlalchemy'
db = SQLAlchemy(app)
app.config['SESSION_SQLALCHEMY'] = db
app.config['SESSION_PERMANENT'] = True
Session(app)
db.create_all()
db.session.commit()

#these are called using normal post request from '(/' route
def Upload_file():
    #create a temp folder with same name as guest username
    if not request.form["key"] == "":
        user_name = session.get('username','not set')
        parent_dir = '/home/oussama/Documents/WORK/PythonWork/Encipherr' #set path
        path = os.path.join(parent_dir, user_name)
        #create temp dir
        os.mkdir(path)
        #---------------
        uploaded_file = request.files["file"]
        uploaded_file.save(os.path.join(path,secure_filename(uploaded_file.filename)))
        filename = secure_filename(uploaded_file.filename)
        #print(filename)
        session["path"]=path
        session["filename"]=filename
        #print("file uploaded")
    else:
        #print("raising error..")
        #key is not important for upload but if there is no key the file will 
        #be uploaded but not encrypted/decrypted therefore the file will not be deleted.
        raise Exception("key not found")    
    
def Encrypt_file():

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

#these are called using ajax
@app.route('/genkey',methods=['GET'])
def genkey():
    key = Fernet.generate_key()
    return key.decode()

@app.route('/encrypttext',methods=['POST'])
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
            return {"status":"0","value":"Error in Encryption!, Possible problems : Key Not Found or Invalid Key"}
    else:
        return {"status":"0","value":"Error! Nothing to encrypt,You have to type something!"}


@app.route('/decrypttext',methods=['POST'])
def Decrypt_Text():
    data = request.get_json()
    if not data["value"] == '':
        try:
            key = data["key"]
            value = data["value"]
            fernet = Fernet(key)
            plaintext = value.encode()
            decryptedtext = fernet.decrypt(plaintext)
            return {"status":"1","value":decryptedtext.decode()}
        except:
            return {"status":"0","value":"Error in Decryption!, Possible problems : Key Not Found or Invalid Key"}
    else:
        return {"status":"0","value":"Error! Nothing to decrypt,You have to type something!"}
        
def SetupGuestSession():
    #setup a guest session when an user enters the website,needed for file upload.
    import string
    user_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    session["username"] = user_name
    session["path"] = ""
    session["filename"] = ""  

@app.route('/',methods=['POST','GET'])
@app.route('/home',methods=['POST','GET'])
def home():
    if request.method == 'POST':
        SetupGuestSession()
        print("setting up guest session")
        if request.form["submit_b"] == "Upload and Encrypt":
            try:
                Upload_file()
                try:
                    filename=Encrypt_file()
                except:
                    flash('Error in Encryption!, Possible problems : Key Not Found Or File Not Found')
                    path = session.get('path','not set')
                    shutil.rmtree(path)
                    return redirect(url_for('home'))  
                
                return redirect(url_for('getfile',file_name=filename))
            except:
                flash('Error!, Possible problems: No File To Upload or Key Not Found!')
                return redirect(url_for('home'))

        elif request.form["submit_b"] == "Upload and Decrypt":
            try:
                Upload_file()
                
                try:
                    filename=Decrypt_file()
                except:
                    flash('Error in Decryption!, Possible problems : Key Not Found,File Not found Or Invalid Key!')
                    path = session.get('path','not set') 
                    shutil.rmtree(path)
                    return redirect(url_for('home'))
                
                return redirect(url_for('getfile',file_name=filename))
            
            except:
                flash('Error!, Possible problems: No File To Upload or Key Not Found ')
                return render_template('home.html')
        else:
            return render_template('home.html')

    else:
        return render_template('home.html')

    
#Return file for downloading,after download it will be deleted with the directory
@app.route("/get-file/<file_name>")
def getfile(file_name):
    path = session.get('path','not set')
    #print(path)
    filename = session.get('filename','not set')
    try:
        @after_this_request
        def remove_file_and_dir(response):
            if os.path.exists(path):
                shutil.rmtree(path)
            session.pop('path')
            session.pop('filename')
            
            return response

        return send_from_directory(directory=path, path=file_name,as_attachment=True,cache_timeout=0)
    except FileNotFoundError:
        abort(404)


@app.route('/sw.js',methods=["GET","POST"])
def service_worker():
    from flask import make_response
    response = make_response(send_from_directory('.',path='sw.js'))
    response.headers['Content-Type'] = 'application/javascript'
    response.headers['Service-Worker-Allowed'] = '/'
    return response

@app.route("/offline")
def offline():
    return render_template('offline.html')
    
@app.route("/about")
def about():
    return render_template('about.html')
@app.route("/privacy")
def privacy():
    return render_template('privacy.html')

if __name__ == '__main__':
    app.run(debug=True) #change host ip
