from jwt import JWT, jwk_from_dict, jwk_from_pem
import httpx

from keys.keys_path_reader import *
from keys.properties_reader import *

def get_JWK_from_local_pub_file():
    with open(get_Public_Key_path(), 'rb') as key_file:
        signing_key = jwk_from_pem(key_file.read())
    #print("JSON from LOCAL pub file:")
    #print(signing_key.to_dict())
    return signing_key

def get_JWK_from_web_pub_file():
    url_response = httpx.get(url="https://www.cm-innovationlab.it/.well-known/" + getValueFromProp('Public_Key_Name') + ".pub")
    signing_key = jwk_from_pem(url_response.content)
    #print("JSON from WEB pub file:")
    #print(signing_key.to_dict())
    return signing_key

def get_JWK_from_web_jwks_json():
    url_response = httpx.get(url="https://www.cm-innovationlab.it/.well-known/jwks.json")
    #print("JSON from WEB JWKS:")
    #print(url_response.json()['keys'][0])
    return jwk_from_dict(url_response.json()['keys'][0])

instance = JWT()

def decode_token(token, type = 0, verify = True):
    message = ""
    try:   
        if (type == 0):
            message = instance.decode(token, get_JWK_from_local_pub_file(), verify, ["RS256"])
        elif (type == 1):
            message = instance.decode(token, get_JWK_from_web_pub_file(), verify, ["RS256"])
        elif (type == 2):
            message = instance.decode(token, get_JWK_from_web_jwks_json(), verify, ["RS256"])
        return {"Decoded Message": str(message), "Verified": verify}

    except Exception as exception:          #jwt.ExpiredSignatureError      jwt.InvalidTokenError
        return {"Exception": str(exception)}    