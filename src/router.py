from flask import Flask, redirect, url_for, request, Response
import requests
from home import homefunc
from callback import auth

app = Flask(__name__)

@app.route("/") #home page 
def mainpg():
    code = request.args.get("code")
    response = Response()
    response.headers['Content-Encoding'] = "gzip"
    response.headers['Vary'] = 'Accept-Encoding'
    return homefunc(code)

@app.route("/login/")
def login():
    return auth()

if __name__ == "__main__":
    app.run(host = "localhost", port=6900, debug=True)
