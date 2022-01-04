from flask import redirect, make_response
from initialize import db, users
import requests
import os, io
import json
import datetime
from dotenv import load_dotenv
load_dotenv()
callbackurl = os.environ.get("CALLBACK_URL")
apikey = os.environ.get("API_KEY")
#apikey_encode = os.environ.get("API_KEY_ENCODED")
def createunixtime():
    today = {
        "year": datetime.datetime.now().year,
        "month": datetime.datetime.now().month,
        "day": datetime.datetime.now().day
    }
    startDate = datetime.datetime(today["year"], today["month"], today["day"], 0) #Start of today
    endDate = datetime.datetime(today["year"], today["month"], today["day"], 23) #End of today

    unix_start = datetime.datetime.timestamp(startDate) *1000
    unix_end = datetime.datetime.timestamp(endDate) *1000
    print("Start: ", int(unix_start))
    print("End: ", int(unix_end))
    return {"start": int(unix_start), "end": int(unix_end)}

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

def get_prices(ticker, usr, interval):
    #TODO: would need to run this function every minute or sum then run the refresh_auth function every 15 mintues
    access = refresh_auth(usr) #Get Access Token with the Refresh token 
    #TODO: This is not optimal ^^^
    time = createunixtime()
    ticker = ticker.upper()
    link = f"https://api.tdameritrade.com/v1/marketdata/{ticker}/pricehistory"
    parameters = {
        "periodType": "day",
        "frequencyType": "minute",
        "frequency": str(interval),
        "endDate": str(time["end"]),
        "startDate": str(time["start"]),
        "needExtendedHoursData": True
    }
    header = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip",
        "Accept-Language": "en-US",
        "Authorization": f"Bearer {access}"
    }
    response = requests.get( 
        link,
        headers=header,
        params=parameters)
    #write the output into a json file in the users respective folder
    output = response.json()
    writeFile(output, ticker, "1", interval) #Span=how many days always going to be 1
    resp = make_response(redirect('/'))
    resp.set_cookie('access_token', access) #set cookie to the login username
    return resp
