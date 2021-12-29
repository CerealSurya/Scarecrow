from flask import Flask, redirect, url_for, request
from router import mainpg

redirect_server = Flask(__name__)

redirectURL = "http://localhost:6900"
@redirect_server.route("/")
def serverREDI():
    code = request.args.get("code")
    output = redirectURL + "?code=" + str(code)
    return redirect(output)
    #return f"<h1>{output}</h1>"

if __name__ == "__main__":
    redirect_server.run(host='localhost', port=1400, ssl_context=('../cert.pem', '../key.pem'))