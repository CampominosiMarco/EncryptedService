from datetime import datetime, timedelta, timezone

from jwt import JWT, jwk_from_pem
from jwt.utils import get_int_from_datetime

from keys.properties_reader import *

def get_JWK_from_private_key():
    with open('keys/'+ getValue('Private_Key_Name', 'keys/properties.properties') + '.pem', 'rb') as key_file:
        signing_key = jwk_from_pem(key_file.read(), bytes(getValue('Password', 'keys/properties.properties'), 'utf-8'))
    return signing_key

instance = JWT()

payload = {
    'iss': 'https://www.cm-innovationlab.it',                                          #issuer (emittente)
    'sub': 'encryptionTest',
    'iat': get_int_from_datetime(datetime.now(timezone.utc)),                           #Issued At (data creazione)
    'exp': get_int_from_datetime(datetime.now(timezone.utc) + timedelta(minutes=30)),
    'name': 'Dinesh',
    'sender_name': "John Doe",
    'admin': True
}

def getEncodedPayload():
    return instance.encode(payload, get_JWK_from_private_key(), alg='RS256')