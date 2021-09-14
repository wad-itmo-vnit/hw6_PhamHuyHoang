from app import app
from flask import render_template,redirect,request,flash, make_response
from app.models.user import User
import os
from functools import wraps
from werkzeug.utils import secure_filename

UPLOAD_FODER = app.config['UPLOAD_FODER'] 


def login (func):
    @wraps(func)
    def loginFunc(*arg, **kwargs):
        try:
            user = User.get_user(request.cookies['username'])
            if user.check_session(request.cookies.get('token')):
                return func(*arg, **kwargs)
        except:
            pass
        flash('login required!')
        return redirect('/signIn')
    return loginFunc

def no_login (func):
    @wraps(func)
    def loginFunc(*arg, **kwargs):
        try:
            user = User.get_user(request.cookies.get('username'))
            if user.check_session(request.cookies.get('token')):
                return redirect('/index')
        except:
            pass
        return  func(*arg, **kwargs)
    return loginFunc

@app.route('/')
def main():
   return redirect('/signIn')

@app.route("/index")
@login
def index():
    return render_template("index.html")

@app.route("/signIn", methods=['POST','GET'])
@no_login
def signIn():
    if request.method == 'GET':
        return render_template('signIn.html')
    elif request.method == 'POST':
        username, password = request.form.get('user'), request.form.get('password')
        user = User(username, password)
        if user.check_username():
            if user.check_password():
                user.generate_session()
                user = User.get_user(username)
                res = make_response(redirect('/index'))
                res.set_cookie('username', user.username)
                res.set_cookie('token', user.token)
                res.set_cookie('avatar', user.avatar)
                print(user.avatar)
                return res
            else:
                flash('Invalid user or password!!!')
                return redirect('/signIn')
        else:
            flash('Invalid user or password!!!')
            return redirect('/signIn')

        
@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if request.method == 'GET':
        return render_template("signUp.html")
    elif request.method == 'POST':
        username, password, confirmPass = request.form.get('user'), request.form.get('password'), request.form.get('confirmPass')
        user = User(username, password)

        if  user.check_username():
            flash('User already exists!!!')
            return redirect('/signUp')

        elif password == confirmPass:
            user.write_data()
            flash("User created successfully!")
            return redirect('/signIn')
        else:
            flash('password dont match!!' )
            return redirect('/signUp') 

@app.route("/logOut")
@login
def logOut():
    user = User.get_user(request.cookies['username'])
    user.delete_session()
    res = make_response(redirect('/signIn'))
    res.delete_cookie('username')
    res.delete_cookie('token')
    res.delete_cookie('avatar')
    return res

@app.route("/changePass", methods=['GET','POST'])
@login
def changePass():
    if request.method == 'GET':
        return render_template("changePass.html")
    
    elif request.method == 'POST':
        currentPassword, newPassword, confirmPassword = request.form.get('currentPass'), request.form.get('newPass'), request.form.get('confirmPass')
        user = User(request.cookies['username'], currentPassword)
        if user.check_password():
            if newPassword == confirmPassword:
                user.update_password(newPassword)
                flash('Successful Change!!!')
                res = make_response(redirect('/signIn'))
                res.delete_cookie('username')
                res.delete_cookie('token')
                return res   
            else:
                flash('Password do not match !!')
                return redirect('/changePass')
        else:
            flash('Invalid password!!!')
            return redirect('/changePass')

@app.route("/upload", methods = ['POST', 'GET'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file!')
            return redirect(request.url)       
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FODER, filename))
        user = User.update_avatar(request.cookies['username'], filename)
        res = make_response(redirect('/index'))
        res.set_cookie('avatar', user.avatar)
        return res   
    return redirect('index')
