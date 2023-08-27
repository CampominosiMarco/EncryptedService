from datetime import datetime, timedelta, timezone
from jwt.utils import get_int_from_datetime

from encode import getEncodedPayload
from decode import decode_token

test_payload = {
    'iss': 'https://www.cm-innovationlab.it',                                          #issuer (emittente)
    'sub': 'encryptionTest',
    'iat': get_int_from_datetime(datetime.now(timezone.utc)),                           #Issued At (data creazione)
    'exp': get_int_from_datetime(datetime.now(timezone.utc) + timedelta(minutes=30)),
    'name': 'Dinesh',
    'sender_name': "John Doe",
    'admin': True
}

#Get token
token = getEncodedPayload(test_payload)
print("Token:\n" + token + "\n")

#Decode token with LOCAL PUB FILE
print("Decoded token with LOCAL PUB FILE:\n" + str(decode_token(token)) + "\n")

#Decode token with WEB PUB FILE
print("Decoded token with WEB PUB FILE:\n" + str(decode_token(token, 1)) + "\n")

#Decode token with WEB JWKS
print("Decoded token with WEB JWKS:\n" + str(decode_token(token, 2)) + "\n")