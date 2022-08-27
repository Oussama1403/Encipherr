""" App Routing """

from flask import Flask,flash,request,render_template,url_for,redirect,send_from_directory,abort,after_this_request,session,stream_with_context
from .app import app
import src.modules
import os,shutil

@app.route('/genkey',methods=['GET'])
def genkey():
    response = src.modules.genkey()
    return response

@app.route('/text',methods=['POST'])
def text_mode():
    data = request.get_json()
    if data["submit_b"] == "Encrypt Text":
        response = src.modules.Encrypt_Text()
        return response
    else:
        response = src.modules.Decrypt_Text()
        return response 

@app.route('/',methods=['POST','GET'])
@app.route('/home',methods=['POST','GET'])
def home():
    """Handle all incoming post/get requests"""
    
    if request.method == 'POST':
        src.modules.SetupGuestSession()
        if request.form["submit_b"] == "Upload and Encrypt":
            try:
                src.modules.Upload_file()
                try:
                    filename=src.modules.Encrypt_file()
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
                src.modules.Upload_file()
                
                try:
                    filename=src.modules.Decrypt_file()
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
                shutil.rmtree(path)
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

@app.route("/about")
def about():
    return render_template('about.html')
@app.route("/privacy")
def privacy():
    return render_template('privacy.html')
