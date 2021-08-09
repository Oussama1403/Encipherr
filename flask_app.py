from flask import Flask,flash,request,render_template,url_for,redirect,send_from_directory,abort,after_this_request
from flask.wrappers import Request
from werkzeug.utils import secure_filename

from cryptography.fernet import Fernet
import os
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

UPLOAD_FOLDER = '/home/oussama/Downloads/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

#these are called using normal post request from '/' route
def Encrypt_file():
    key = request.form["key"]
    fernet = Fernet(key)
    with open(os.path.join(app.config['UPLOAD_FOLDER'],filename) , 'rb') as f:
        data = f.read()
    encryptedfile = fernet.encrypt(data)
    with open(os.path.join(app.config['UPLOAD_FOLDER'],filename),'wb') as f:
        f.write(encryptedfile)
    return filename

def Decrypt_file():
    key = request.form["key"]
    fernet = Fernet(key)
    with open(os.path.join(app.config['UPLOAD_FOLDER'],filename) , 'rb') as f:
        data = f.read()
    decryptedfile = fernet.decrypt(data)
    with open(os.path.join(app.config['UPLOAD_FOLDER'],filename),'wb') as f:
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
            return {"status":"1","value":encryptedtext}
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
            return {"status":"1","value":decryptedtext}
        except:
            return {"status":"0","value":"Error in Decryption!, Possible problems : Key Not Found or Invalid Key"}
    else:
        return {"status":"0","value":"Error! Nothing to decrypt,You have to type something!"}
        
    
@app.route('/',methods=['POST','GET'])
@app.route('/home',methods=['POST','GET'])
def home():
    if request.method == 'POST':
        global filename

        if request.form["submit_b"] == "Upload Selected File":
            try:
                uploaded_file = request.files["file"]
                uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(uploaded_file.filename)))
                filename = secure_filename(uploaded_file.filename)
                print(filename)
                print('file uploaded successfully')
                key = request.form["key"]
                print('file readed successfully')
                flash('File uploaded successfully!')
                return render_template('home.html',key = key)
            except:
                flash('Error!, Possible problems: No File To Upload!')
                return redirect(url_for('home'))

        elif request.form["submit_b"] == "Encrypt File":
            try:
                filename=Encrypt_file()
                return redirect(url_for('getfile',file_name=filename))
            except:
                flash('Error in Encryption!, Possible problems : Key Not Found Or File Not Found')
                return redirect(url_for('home'))
        elif request.form["submit_b"] == "Decrypt File":
            try:
                filename=Decrypt_file()
                return redirect(url_for('getfile',file_name=filename))
            except:
                flash('Error in Decryption!, Possible problems : Key Not Found,File Not found Or Invalid Key!')
                return redirect(url_for('home'))
        else:
            return render_template('home.html')

    else:
        """
        random number to append at <script src="ajaxcall.js"/> and <link ..style.css/> Tags
        to prevent caching css and js file.
        """
        import random
        id = random.randint(0,1000)
        return render_template('home.html',id=id)


#Return file for downloading,after download it will be deleted.
@app.route("/get-file/<file_name>")
def getfile(file_name):
    try:
        @after_this_request
        def remove_file(response):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return response

        return send_from_directory(app.config["UPLOAD_FOLDER"], filename=file_name,as_attachment=True,cache_timeout=0)
    except FileNotFoundError:
        abort(404)


@app.route("/about")
def about():
    return render_template('about.html')
@app.route("/privacy")
def privacy():
    return render_template('privacy.html')

if __name__ == '__main__':
    app.run(host='192.168.1.8',debug=True) #change host ip to yours
