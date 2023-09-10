from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from jwt import jwk_from_pem
import json
from properties_reader import *
from keys_path_reader import *

import os

this_script_dir = os.path.dirname(os.path.abspath(__file__))    #Absolute Path of current script

private_key = rsa.generate_private_key( #https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#rsa
    public_exponent=65537,
    key_size=4096           #1024 and below are considered breakable while 2048 or 4096 are reasonable default key sizes for new keys.
)

private_key_pass = bytes(getValueFromProp('Password'), 'utf-8')

#ENCRYPTED PRIVATE KEY
encrypted_pem_private_key = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.BestAvailableEncryption(private_key_pass)
    #encryption_algorithm=serialization.NoEncryption()
)

#PUBLIC KEY
pem_public_key = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

private_key_file = open(get_Private_Key_path(), "w")
private_key_file.write(encrypted_pem_private_key.decode())
private_key_file.close()

public_key_file = open(get_Public_Key_path(), "w")
public_key_file.write(pem_public_key.decode())
public_key_file.close()

dict_from_pub_pem = jwk_from_pem(pem_public_key).to_dict()
dict_from_pub_pem["alg"] = "RS256"
dict_from_pub_pem["use"] = "sig"
dict_from_pub_pem["kid"] = "CM-InnovationLab.it-1"

JSON_Web_Key_Set = open(get_jwks_path(), "w")
JSON_Web_Key_Set.write(json.dumps({"keys": [dict_from_pub_pem]}))
JSON_Web_Key_Set.close()

# AES KEY implementation
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64

kdf = PBKDF2HMAC(
    algorithm = hashes.SHA256(),
    iterations = 100000,
    salt = os.urandom(16),          # Random value to improve security
    length = 32
)

AES_key = base64.urlsafe_b64encode(kdf.derive(private_key_pass))

with open(get_AES_Key_path(), 'wb') as file:
    file.write(AES_key)