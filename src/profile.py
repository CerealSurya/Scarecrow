from flask import redirect, url_for, request, render_template, Response, make_response
import urllib.parse
import requests
import json
import os
from initialize import db, users

from dotenv import load_dotenv
load_dotenv()

callbackurl = os.environ.get("CALLBACK_URL")
apikey = os.environ.get("API_KEY")

def redirectfunc(): #redirect to url
    callbackUrl_encoded = urllib.parse.quote(callbackurl)
    apikey_encoded = urllib.parse.quote(apikey) #encodes the neccary items
    #creates redirect URL
    return redirect(f"https://auth.tdameritrade.com/auth?response_type=code&redirect_uri={callbackUrl_encoded}&client_id={apikey_encoded}")

def daprofile(username):
    if request.method == 'POST':
            if "home_btn" in request.form:
                return redirect('/')
            elif "logout_btn" in request.form:
                res = make_response(redirect('/'))
                res.set_cookie('userID', 'sum_value', max_age=0)
                return res
            elif "td_btn" in request.form: #get Refresh & Access Token
                return redirectfunc()

    elif request.method == 'GET':
        if username == "" or username == None:
            return render_template('profile.html', username="Login or create an account", email="", password="")
        else:
            usr = users.query.filter_by(username=username).first()
            access = request.cookies.get('access_token')
            if usr == None:
                return render_template('profile.html', username="Login or create an account", email="", password="")
            else:
                return render_template('profile.html', username=username, email=usr.email, password=usr.password, refresh_token=usr.refresh_token, access_token=access)