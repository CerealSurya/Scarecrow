from flask import redirect, url_for, request
import urllib.parse
import os
from dotenv import load_dotenv
load_dotenv()

apikey = os.environ.get("API_KEY")
callbackurl = os.environ.get("CALLBACK_URL")

def getRedirect():
    callbackUrl_encoded = urllib.parse.quote(callbackurl)
    apikey_encoded = urllib.parse.quote(apikey) #encodes the neccary items
    #creates redirect URL
    return f"https://auth.tdameritrade.com/auth?response_type=code&redirect_uri={callbackUrl_encoded}&client_id={apikey_encoded}"

def auth(): #redirect to url
    return redirect(getRedirect())

    
