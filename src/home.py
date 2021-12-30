from flask import Flask, redirect, url_for, render_template, request
import urllib.parse
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

callbackURI = os.environ.get("CALLBACK_URL")
apikey = os.environ.get("API_KEY")

def call_auth(code, apikey, callbackURI):
    parameters = {
        "grant_type": "authorization_code",
        "access_type": "offline",
        "code": str(code),
        "client_id": str(apikey),
        "redirect_uri": callbackURI
    }
    response = requests.post("https://api.tdameritrade.com/v1/oauth2/token", params=parameters)
    print(parameters)
    print(response.json())

def homefunc(code):
    if code is None: 
        return render_template("home.html", code = "")
    elif code is not None: #there is an actual thing in there
        newCode = urllib.parse.unquote(code) #decoding the code
        newCode = str(newCode)
        newCode = "".join( newCode.splitlines())
        call_auth(newCode, apikey, callbackURI)
        return render_template("home.html", code = newCode)
    else:
        return "<h1>Error</h1>"
