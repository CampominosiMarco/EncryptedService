from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from properties_reader import *

private_key = rsa.generate_private_key( #https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#rsa
    public_exponent=65537,
    key_size=4096           #1024 and below are considered breakable while 2048 or 4096 are reasonable default key sizes for new keys.
)

private_key_pass = bytes(getValue('Password'), 'utf-8')

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

private_key_file = open(getValue('Private_Key_Name') + ".pem", "w")
private_key_file.write(encrypted_pem_private_key.decode())
private_key_file.close()

public_key_file = open(getValue('Public_Key_Name') + ".pub", "w")
public_key_file.write(pem_public_key.decode())
public_key_file.close()