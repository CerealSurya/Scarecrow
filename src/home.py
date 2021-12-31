from flask import Flask, redirect, url_for, render_template, request
import urllib.parse
import requests
import json
import os
from initialize import db, users

from dotenv import load_dotenv
load_dotenv()

callbackurl = os.environ.get("CALLBACK_URL")

def auth(): #redirect to url
    callbackUrl_encoded = urllib.parse.quote(callbackurl)
    apikey_encoded = urllib.parse.quote(apikey) #encodes the neccary items
    #creates redirect URL
    return redirect(f"https://auth.tdameritrade.com/auth?response_type=code&redirect_uri={callbackUrl_encoded}&client_id={apikey_encoded}")

callbackURI = os.environ.get("CALLBACK_URL")
apikey = os.environ.get("API_KEY")

def call_auth(code, apikey, callbackURI):
    parameters = {
        "grant_type": "authorization_code",
        "refresh_token": "",
        "access_type": "offline",
        "code": str(code),
        "client_id": str(apikey),
        "redirect_uri": str(callbackURI)
    }
    response = requests.post("https://api.tdameritrade.com/v1/oauth2/token", 
    data=parameters)
    output = response.json()
    access_token = output["access_token"]
    refresh_token = output["refresh_token"]
    print("Access_Token: ", access_token)
    print("Refresh_Token: ", refresh_token)

def homefunc(code, user):
    username = user.username
    email = user.email
    if code is None:
        return render_template("home.html", code = "", username=username, email=email)
    elif code is not None: #don't need to decode it because browser already does it
        newCode = str(code)
        newCode = newCode.replace(" ", "+")
        call_auth(newCode, apikey, callbackURI)
        return render_template("home.html", code = newCode, username=username, email=email)
    else:
        return "<h1>Error</h1>"
