from flask import Flask, request
from flask_cors import CORS

import json
import base64
import array

from datetime import datetime, timedelta, timezone
from jwt.utils import get_int_from_datetime

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

#ONLY for this files configuration, you can import script how you want
import os
import sys
server_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(server_dir)
upper_parent_dir = os.path.dirname(parent_dir)
sys.path.append(upper_parent_dir)

from encode import getEncodedPayload
from decode import decode_token
from keys.keys_reader_writer import *

#This is AES key to encrypt or decrypt payload
aes_key_byte_array = base64.urlsafe_b64decode(read_AES_Key())

#Function to convert dictionary from payload in byte array
def convertDictionaryToByteArray(dict):
    output_lists = []
    for key, value in dict.items():
        output_lists.append(value)
    return array.array('B', output_lists)

myEndPoint = Flask(__name__)
cors = CORS(myEndPoint)

@myEndPoint.route("/test", methods = ['GET'])
def test():
    return {"status": "Service Up!"}, 200


@myEndPoint.route("/login", methods = ['POST'])
def login():    #of course this is only a test :)
    json_data = request.get_json()
    payload_checked, code = payload_check(json_data)

    if code != 200:
        return payload_checked, code

    if (payload_checked['username'] == "marco.campominosi" and payload_checked['password'] == "enjoy"):

        now = datetime.now(timezone.utc)
        expiration = get_int_from_datetime(now + timedelta(minutes=30))

        token = getEncodedPayload({'exp': expiration,
                                'username': payload_checked['username'],
                                'user_id': 7285,
                                'admin': 'true'})
        
        response_payload = {
                            'iss': 'http://www.cm-innovationlab.it:5002',
                            'sub': 'encryptionTest',
                            #'iat': get_int_from_datetime(now),
                            #'exp': expiration,
                            'token': token
                            }
        return {"content": response_payload}, 200
    return {"error": "Login Error!"}, 401


@myEndPoint.route("/message_receiver", methods = ['POST'])
def message_receiver():

    #First of all verify Token!
    token_msg, code = token_validation(request.headers['Authorization'][7:])

    if code == 500:
        return token_msg, code
    elif code == 401:
        return token_msg, code
    
    print("Good Request!\n- Verified: " + str(token_msg["Verified"]) + "\n- Decoded Message: " + token_msg["Decoded Message"])

    #Now check request
    json_data = request.get_json()
    payload_checked, code = payload_check(json_data)

    if "message" in payload_checked:
        decoded_msg_tkn = json.loads(token_msg["Decoded Message"].replace("'", "\""))
        expiration = decoded_msg_tkn["exp"]
        now = get_int_from_datetime(datetime.now(timezone.utc))
        timestamp_int = expiration - now
        minuti_rimasti = (timestamp_int % 3600) // 60

        return {"content": payload_checked["message"][::-1],
                "remaining_time": minuti_rimasti,
                "request_owner": decoded_msg_tkn['username']}, 200
    return {"error": "Check Message!"}, 400


def payload_check(json_data):
    if len(json_data) == 2 and "byte_array" in json_data and "iv" in json_data:

        byte_array = json_data["byte_array"]
        iv = json_data["iv"]
        
        if isinstance(byte_array, dict) and isinstance(iv, dict):

            try:
                byte_array = convertDictionaryToByteArray(byte_array)
                iv = convertDictionaryToByteArray(iv)

                cipher = Cipher(algorithms.AES(aes_key_byte_array), modes.CBC(iv))
                decryptor = cipher.decryptor()

                decrypted_data = decryptor.update(byte_array) + decryptor.finalize()

                while not decrypted_data.endswith(b'}'): #remove last bytes such as '\x01' '\x03'
                    decrypted_data = decrypted_data[:-1]

                json_str = decrypted_data.decode('utf-8')
                jsonMsg = json.loads(json_str)

                return jsonMsg, 200

            except Exception as e:
                return {"error": str(e)}, 500
            
        else:
            return {"error": "Check payload type!"}, 400
        
    else:
        return {"error": "Check payload!"}, 400


def token_validation(token_passed):
    try:
        if token_passed != '' and token_passed != None:
            data_json = decode_token(token_passed, 1)

            if len(data_json) == 2 and "Decoded Message" in data_json and "Verified" in data_json:
                return data_json, 200
            else:
                return {"error" : data_json["Exception"]}, 401
        else:
            return {"error" : "Token required!"}, 401
    except Exception as e:
        return {"error" : "An error occured!" + str(e)}, 500