from flask import Flask, redirect, url_for, request, Response, render_template, make_response
from initialize import app, db, users
from home import homefunc, startup
from account import loginfunc
import os
from dotenv import load_dotenv
from profile import daprofile
load_dotenv()

mainurl = os.environ.get("MAIN_URL")

@app.route("/", methods=["POST", "GET"] ) #home page 
def mainpg():
    return startup()

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
    return daprofile(username)

if __name__ == "__main__":
    db.create_all()
    app.run(host = "localhost", port=6900, debug=True)
