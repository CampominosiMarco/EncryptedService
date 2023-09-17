from flask import Flask, request
from flask_cors import CORS

import json
import base64
import array
import numpy as np

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
                decrypted_data = decrypted_data[:-1]    #remove last '\x01'

                json_str = decrypted_data.decode('utf-8')
                jsonMsg = json.loads(json_str)

                if (jsonMsg['username'] == "marco.campominosi" and jsonMsg['password'] == "enjoy"):

                    now = datetime.now(timezone.utc)
                    expiration = get_int_from_datetime(now + timedelta(minutes=30))

                    token = getEncodedPayload({'exp': expiration,
                                            'username': jsonMsg['username'],
                                            'user_id': 7285,
                                            'admin': True})
                    
                    response_payload = {
                                        'iss': 'http://www.cm-innovationlab.it:5002',
                                        'sub': 'encryptionTest',
                                        #'iat': get_int_from_datetime(now),
                                        #'exp': expiration,
                                        'token': token
                                        }
                    return {"content": response_payload}, 200
                return {"error": "Login Error!"}, 401

            except Exception as e:
                return {"error": str(e)}, 500
            
        else:
            return {"error": "Check payload type!"}, 400
        
    else:
        return {"error": "Check payload!"}, 400














@myEndPoint.route("/message_receiver", methods = ['POST'])
def message_receiver():





    msg, code = token_validation(request.headers['Authorization'][7:])



    json_data = request.get_json()


    #prendere messaggio
    #prendere nome dal token
    #prendere il tempo rimanente


    if (json_data['array'] != None):

    #    print(np.asarray(list(x[1] for x in json_data['array'].items())))
        arr = np.array(list(x[1] for x in json_data['array'].items()), dtype=np.uint8)



       # array_view = arr.view(f'S{arr.shape[0]}')

        return {"content": msg, "array_resp" : arr.tolist()}, code        #''.join(map(chr, arr))
    return {"error": "Array Error!"}, 401



def token_validation(token_passed):
    try:
        if token_passed != '' and token_passed != None:
            data = decode_token(token_passed, 2)    #serve la dec con chiave privata magari 3
            return data, 200
        else:
            return {"error" : "Token required!"}, 401
    except Exception as e:
        return {"error" : "An error occured!" + str(e)}, 500


