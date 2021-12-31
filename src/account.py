from flask import redirect, url_for, request, render_template, Response, make_response
import urllib.parse
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
            find_user = users.query.filter_by(username=un, password=passw).first()
            if find_user != None: 
                resp = make_response(redirect('/'))
                resp.set_cookie('userID', find_user.username, expires=datetime.datetime.now() + datetime.timedelta(days=30) ) #set cookie to the login username
                return resp
            else:
                return render_template('login.html', heading="Error login credentials invalid try create new account", createacc_link=mainurl + "/createaccount")
    # elif "Create Account" in request.data:
    #     return redirect(mainurl + "/createaccount")