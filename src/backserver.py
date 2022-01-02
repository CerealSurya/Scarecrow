from flask import Flask, redirect, url_for, request
from router import mainpg
import os
from dotenv import load_dotenv
load_dotenv()

mainurl = os.environ.get("MAIN_URL")

redirect_server = Flask(__name__)

@redirect_server.route("/")
def serverREDI():
    code = request.args.get("code")
    output = f"{mainurl}?code={str(code)}"
   # output = mainurl + "?code=" + str(code)
    return redirect(output)

if __name__ == "__main__":
    redirect_server.run(host='localhost', port=1400, ssl_context=('../cert.pem', '../key.pem'))