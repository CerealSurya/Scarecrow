from flask import Flask, redirect, url_for, request, Response, render_template, make_response
from initialize import app, db, users
from home import homefunc
from account import loginfunc
import os
from dotenv import load_dotenv
load_dotenv()


mainurl = os.environ.get("MAIN_URL")

@app.route("/", methods=["POST", "GET"] ) #home page 
def mainpg():
    name = request.cookies.get('userID')
    if request.method == 'POST':
        if 'logoutbtn' in request.form:
            res = make_response(redirect('/'))
            res.set_cookie('userID', 'sum_value', max_age=0)
            return res
        elif request.form['profilebtn'] == 'Profile':
            find_user = users.query.filter_by(username=name).first()
            return redirect(url_for('profilefunc', username=find_user.username))                   #(f"/profile/{find_user.username}")
        else:
            return "<h1>Error</h1>"
    elif request.method == 'GET':
        if name == None: #if there is no cookie that has UserID to compare 
            return redirect('/login')
        else:
            find_user = users.query.filter_by(username=name).first()
            if find_user: #if the user already has an account
                code = request.args.get("code")
                response = Response()
                response.headers['Content-Encoding'] = "gzip"
                response.headers['Vary'] = 'Accept-Encoding'
                return homefunc(code, find_user)
            else: #put a clear cookie thing here maybe
                return "<h1>Error</h1>"

@app.route("/login/", methods=["POST", "GET"]) #login page
def login():
    if request.method == 'POST': #login page
        return loginfunc()
    elif request.method == 'GET':
        return render_template('login.html', heading="Login to Scarecrow Account", createacc_link=mainurl + "/createaccount")

@app.route("/createaccount/", methods=["POST", "GET"])
def createaccount():
    if request.method == 'POST':
        if "submit_account" in request.form:
            un = request.form["un"]
            email = request.form["ea"]
            passw = request.form["pass"]
            find_user_un = users.query.filter_by(username=un).first()
            find_user_ea = users.query.filter_by(email=email).first()
            if find_user_un: #there already is an account with the information meaning they need to login
                return render_template('createaccount.html', acc_info="Username is already taken", login_link=mainurl + "/login")
            if find_user_ea:
                return render_template('createaccount.html', acc_info="Email Address is already in use", login_link=mainurl + "/login")
            else: #Create new account, Inseert the form data into the database and redirect them to login
                usr = users(un, email, passw, "") #blank string for refresh token
                db.session.add(usr)
                db.session.commit()
                return redirect("/login")
    elif request.method == 'GET':
        return render_template('createaccount.html', heading="Create Scarecrow Account", acc_info="", login_link=mainurl + "/login")

@app.route("/<username>/", methods=["POST", "GET"])
def profilefunc(username): #username is going to be the find_user in the db
    if request.method == 'POST':
        return "<h1>hi</h1>"
    elif request.method == 'GET':
        if username == "" or username == None:
            return render_template('profile.html', username="Login or create an account", email="", password="")
        else:
            usr = users.query.filter_by(username=username).first()
            return render_template('profile.html', username=username, email=usr.email, password=usr.password)

if __name__ == "__main__":
    db.create_all()
    app.run(host = "localhost", port=6900, debug=True)
