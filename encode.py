from jwt import JWT, jwk_from_pem

from keys.properties_reader import *

def get_JWK_from_private_key():
    with open('keys/'+ getValue('Private_Key_Name', 'keys/properties.properties') + '.pem', 'rb') as key_file:
        signing_key = jwk_from_pem(key_file.read(), bytes(getValue('Password', 'keys/properties.properties'), 'utf-8'))
    return signing_key

def getEncodedPayload(payload):
    return JWT().encode(payload, get_JWK_from_private_key(), alg='RS256')