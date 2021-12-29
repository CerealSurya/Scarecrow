
from flask import Flask, redirect, url_for, render_template, request
import urllib.parse
    
def homefunc(code):
    if code is None: 
        return render_template("home.html", code = "")
    elif code is not None: #there is an actual thing in there
        newCode = urllib.parse.unquote(code)
        return render_template("home.html", code = newCode)
    else:
        return "<h1>Error</h1>"
