from flask import Flask, redirect, url_for, render_template, request, make_response, Response
from initialize import db, users
import urllib.parse
import requests
import os
import datetime
from dotenv import load_dotenv

load_dotenv()
callbackurl = os.environ.get("CALLBACK_URL")
apikey = os.environ.get("API_KEY")

def call_auth(code, apikey, callbackurl, user):
    parameters = {
        "grant_type": "authorization_code",
        "refresh_token": "",
        "access_type": "offline",
        "code": str(code),
        "client_id": str(apikey),
        "redirect_uri": str(callbackurl)
    }
    response = requests.post("https://api.tdameritrade.com/v1/oauth2/token", 
    data=parameters)
    output = response.json()

    access_token = output["access_token"]
    refresh_token = output["refresh_token"]

    user.refresh_token = refresh_token
    db.session.commit()
    print("Access_Token: ", access_token)
    print("Refresh_Token: ", user.refresh_token)
    #setting access token cookie
    resp = make_response(redirect('/'))
    resp.set_cookie('access_token', access_token ) 
    return resp

def homefunc(code, user):
    username = user.username
    email = user.email
    if code is None:
        return render_template("home.html", username=username, email=email)
    elif code is not None: #don't need to decode it because browser already does it
        newCode = str(code)
        newCode = newCode.replace(" ", "+")
        return call_auth(newCode, apikey, callbackurl, user)
    else:
        return "<h1>Error</h1>"

def startup():
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