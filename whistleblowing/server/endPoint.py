from flask import Flask, request
from flask_cors import CORS

import json

from datetime import datetime, timedelta, timezone
from jwt.utils import get_int_from_datetime

import os
import sys
server_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(server_dir)
upper_parent_dir = os.path.dirname(parent_dir)
sys.path.append(upper_parent_dir)

from encode import getEncodedPayload
from decode import decode_token

myEndPoint = Flask(__name__)
cors = CORS(myEndPoint)

@myEndPoint.route("/test", methods = ['GET'])
def test():
    return {"status": "Service Up!"}, 200




@myEndPoint.route("/login", methods = ['POST'])
def login():    #of course this is only a test :)
    json_data = request.get_json()
    if (json_data['username'] == "marco.campominosi" and json_data['password'] == "enjoy"):

        now = datetime.now(timezone.utc)
        expiration = get_int_from_datetime(now + timedelta(minutes=30))

        token = getEncodedPayload({'exp': expiration,
                                   'username': json_data['username'],
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





import numpy as np


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



'''





#chatgpt


import json
import os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hmac
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding




username = 'pino'
password = 'strampalato'
user_data = {'username': username, 'password': password}
json_text = json.dumps(user_data)

print('\nUser Data:', user_data, ' - JSON Text:', json_text)

iv = os.urandom(16)  # Genera un vettore di inizializzazione (IV) casuale
cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv), backend=default_backend())
encryptor = cipher.encryptor()

# Salva l'IV insieme ai dati cifrati
encrypted_data = iv + encryptor.update(json_text.encode('utf-8')) + encryptor.finalize()

# 3. Firma digitalmente il JSON cifrato con la chiave privata RSA
signature = private_key.sign(
    encrypted_data,
    padding.PKCS1v15(),
    hashes.SHA256()
)

# Ora hai il JSON cifrato, la firma digitale e la chiave pubblica RSA per la verifica
print('\nIV:', iv)
print('\nIV concat a JSON cifrato:', encrypted_data)
print('\nFirma digitale:', signature)
print('\nChiave pubblica RSA:', public_key)

# Per verificare la firma digitale con la chiave pubblica RSA
is_verified = public_key.verify(
    signature,
    encrypted_data,
    padding.PKCS1v15(),
    hashes.SHA256()
)

if is_verified:
    print('\nLa firma è verificata!')
    # 2. La firma è valida, ora puoi decifrare i dati cifrati con la chiave simmetrica AES

    iv_decryption = encrypted_data[:16]
    encrypted_text = encrypted_data[16:]

    cipher = Cipher(algorithms.AES(loaded_symmetric_key), modes.CFB(iv_decryption), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_text) + decryptor.finalize()

    # 3. Hai ora il JSON originale
    original_data = json.loads(decrypted_data.decode('utf-8'))

    print('\nDati originali:', original_data)
else:
    print('\nFirma non valida. I dati potrebbero essere stati alterati.')
















'''