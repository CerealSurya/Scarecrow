from flask import Flask, redirect, url_for, render_template, request, make_response, Response
from initialize import db, users
import requests
import os, io
import json
from dotenv import load_dotenv
load_dotenv()
callbackurl = os.environ.get("CALLBACK_URL")
apikey = os.environ.get("API_KEY")

def writeFile(info, ticker, span, interval):
    folder_path = os.path.abspath('./data')
    file_path = f"{ticker}_{span}_{interval}.json"
    path_exists = os.path.exists(folder_path+file_path)
    try:
        if not path_exists: #Creates the user's folder used for storing .json data
            with io.open(os.path.join(folder_path, file_path), 'w') as db_file:
                db_file.write(json.dump(info, db_file, ensure_ascii=False, indent=4 ))
            print(f"{ticker}.json created")
        else:
            with io.open(folder_path + file_path, 'w') as db_file:
                db_file.write(json.dump(info, db_file, ensure_ascii=False, indent=4))
    except:
        return

def refresh_auth(usr):
    parameters = {
        "grant_type": "refresh_token",
        "refresh_token": usr.refresh_token,
        "client_id": apikey,
    }
    response = requests.post("https://api.tdameritrade.com/v1/oauth2/token", data=parameters)
    output = response.json()
    print(output)
    return output["access_token"]

def get_prices(ticker, usr, span, interval):
    access = refresh_auth(usr) #Get Access Token with the Refresh token 
    #TODO: This is not optimal ^^^
    ticker = ticker.upper()
    parameters = {
        "apikey": apikey,
        "periodType": "day",
        "period": span,
        "frequencyType": "minute",
        "frequency": interval
    }
    header = {
        "Authorization": f"Bearer {access}"
    }
    response = requests.get( 
        f"https://api.tdameritrade.com/v1/marketdata/{ticker}/pricehistory",
        headers=header,
        data=parameters)
    #write the output into a json file in the users respective folder
    output = response.json()
    writeFile(output, ticker, span, interval)
    print(output)
    resp = make_response(redirect('/'))
    resp.set_cookie('access_token', access) #set cookie to the login username
    return resp

def call_auth(code, user):
    parameters = {
        "grant_type": "authorization_code",
        "refresh_token": "",
        "access_type": "offline",
        "code": str(code),
        "client_id": str(apikey),
        "redirect_uri": str(callbackurl)
    }
    response = requests.post("https://api.tdameritrade.com/v1/oauth2/token", data=parameters)
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
        return call_auth(newCode, user)
    else:
        return "<h1>Error</h1>"

def startup():
    name = request.cookies.get('userID')
    if request.method == 'POST':
        find_user = users.query.filter_by(username=name).first()
        if 'logoutbtn' in request.form:
            res = make_response(redirect('/'))
            res.set_cookie('userID', 'sum_value', max_age=0)
            return res
        elif "profilebtn" in request.form:
            return redirect(url_for('profilefunc', username=find_user.username))                   #(f"/profile/{find_user.username}")
        elif "get_prices" in request.form:
            ticker = request.form["ticker"]
            span = 1
            interval = 15
            return get_prices(ticker, find_user, span, interval)
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