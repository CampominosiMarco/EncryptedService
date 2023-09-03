from flask import Flask, request
from flask_cors import CORS

import json

from datetime import datetime, timedelta, timezone
from jwt.utils import get_int_from_datetime

from scripts.encode import getEncodedPayload
from scripts.decode import decode_token





myEndPoint = Flask(__name__)
cors = CORS(myEndPoint)




@myEndPoint.route("/test", methods = ['GET'])
def test():
    return {"status": "Service Up!"}, 200




@myEndPoint.route("/login", methods = ['POST'])
def login():    #of course this is only a test :)
    json_data = request.get_json()
    if (json_data['username'] == "marco.campominosi" and json_data['password'] == "enjoy"):

        now = get_int_from_datetime(datetime.now(timezone.utc))
        expiration = get_int_from_datetime(datetime.now(timezone.utc) + timedelta(minutes=30))

        token = getEncodedPayload({'exp': expiration, 'username': json_data['username'], 'admin': True})
        
        response_payload = {
                            'iss': 'https://www.cm-innovationlab.it:5002',
                            'sub': 'encryptionTest',
                            'iat': now,
                            'exp': expiration,
                            'token': token
                        }
        return {"content": response_payload}, 200
    return {"error": "Login Error!"}, 401








@myEndPoint.route("/message_receiver", methods = ['POST'])
def message_receiver():





token_validation()



    json_data = request.get_json()


    #prendere messaggio
    #prendere nome dal token
    #prendere il tempo rimanente


    if (json_data['message'] != None):
        test_payload = {
                            'iss': 'https://www.cm-innovationlab.it:5002',
                            'sub': 'encryptionTest',
                            'iat': get_int_from_datetime(datetime.now(timezone.utc)),
                            'exp': get_int_from_datetime(datetime.now(timezone.utc) + timedelta(minutes=30)),
                            'username': 'marco.campominosi',
                            'admin': True
                        }
        return {"content": getEncodedPayload(test_payload)}, 200
    return {"error": "Message Error!"}, 401



def token_validation():
    try:
        token_passed = request.headers['token']
        if token_passed != '' and token_passed != None:
            data = decode_token(token_passed, 3)    #serve la dec con chiave privata
            return myEndPoint.response_class(response=json.dumps(data), mimetype='application/json'),200
        else:
            return myEndPoint.response_class(response=json.dumps({"error" : "Token required!"}), mimetype='application/json'),401
    except Exception as e:
        return myEndPoint.response_class(response=json.dumps({"error" : "An error occured!"}), mimetype='application/json'),500

