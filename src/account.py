from flask import redirect, request, render_template, make_response
import os
from dotenv import load_dotenv
from initialize import db, users
import datetime
load_dotenv()

apikey = os.environ.get("API_KEY")
callbackurl = os.environ.get("CALLBACK_URL")
mainurl = os.environ.get("MAIN_URL")  

def loginfunc():
    if "submit_login" in request.form:
            un = request.form["un"]
            passw = request.form["pass"]
            find_user = users.query.filter_by(username=un).first() #finds based on username
            if find_user == None: #If there is no user fouund with that username
                return render_template('login.html', heading="No username that matches that", createacc_link=mainurl + "/createaccount")
            else:
                right_password = users.validate(passw, find_user.password)
                if right_password:
                    resp = make_response(redirect('/'))
                    resp.set_cookie('userID', find_user.username, expires=datetime.datetime.now() + datetime.timedelta(days=30) ) #set cookie to the login username
                    return resp
                else:
                    return render_template('login.html', heading="Incorrect Password", createacc_link=mainurl + "/createaccount")

    # elif "Create Account" in request.data:
    #     return redirect(mainurl + "/createaccount")