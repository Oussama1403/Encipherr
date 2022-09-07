""" App Routing """

from flask import flash,request,render_template,url_for,redirect,send_from_directory,abort,after_this_request,session
from .app import app
from src.modules import TextEncryption,FileEncryption,Utils
import os,shutil

@app.route('/genkey',methods=['GET'])
def genkey():
    return Utils.genkey()

@app.route('/text',methods=['POST'])
def text_mode():
    data = request.get_json() 

    text = TextEncryption()
    
    if data["submit_b"] == "Encrypt Text":
        response = text.encrypt()
        return response
    else:
        response = text.decrypt()
        return response 


@app.route('/',methods=['GET'])
def base():
    return redirect(url_for('home'))

@app.route('/home',methods=['POST','GET'])
def home():
    """Handle all incoming post/get requests"""
    
    if request.method == 'POST':
        Utils.SetupGuestSession()
        if request.form["submit_b"] == "Upload and Encrypt":
            try:
                Utils.Upload_file()
                try:
                    file = FileEncryption()
                    filename=file.encrypt()
                except:
                    flash('Encryption failed! , possible problem: key not found or invalid key')
                    path = session.get('path','not set')
                    shutil.rmtree(path)
                    return redirect(url_for('home'))  
                
                return redirect(url_for('getfile',file_name=filename))
            except:
                flash('Upload failed! , possible problem: no file to upload or key not found')
                return redirect(url_for('home'))

        elif request.form["submit_b"] == "Upload and Decrypt":
            try:
                Utils.Upload_file()
                
                try:
                    file = FileEncryption()
                    filename=file.decrypt()
                except:
                    flash('Decryption failed! , possible problem: key not found or invalid key')
                    path = session.get('path','not set') 
                    shutil.rmtree(path)
                    return redirect(url_for('home'))
                
                return redirect(url_for('getfile',file_name=filename))
            
            except:
                flash('Upload failed! , possible problem: no file to upload or key not found')
                return render_template('home.html')
        else:
            return render_template('home.html')

    else:
        return render_template('home.html')

@app.route("/get-file/<file_name>")
def getfile(file_name):
    """Return file for downloading,after download it will be deleted with the directory"""
    path = session.get('path','not set')
    #print(path)
    filename = session.get('filename','not set')
    try:
        @after_this_request
        def remove_file_and_dir(response):
            if os.path.exists(path):
                if app.config["ENV"] == "DEV":
                    shutil.rmtree(path)
                else:
                    # Delete only the file without its dir to avoid 
                    # OSError: [Errno 16] Device or resource busy: '.nfs0000000005..' prod error.
                    os.remove(os.path.join(path,filename))
            session.pop('path')
            session.pop('filename')
            
            return response

        return send_from_directory(directory=path, path=file_name,as_attachment=True,max_age=0)
    except FileNotFoundError:
        abort(404)

@app.route('/sw.js',methods=["GET","POST"])
def service_worker():
    from flask import make_response
    response = make_response(send_from_directory('.',path='sw.js'))
    response.headers['Content-Type'] = 'application/javascript'
    response.headers['Service-Worker-Allowed'] = '/'
    return response

@app.route('/robots.txt',methods=["GET"])
def robots_file():
    from flask import make_response
    response = make_response(send_from_directory('.',path='robots.txt'))
    response.headers["Content-type"] = "text/plain"
    return response
    
@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/privacy")
def privacy():
    return render_template('privacy.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template("page-404.html"), 404

@app.errorhandler(500)
def server_error(error):
    return render_template("page-500.html"), 500
