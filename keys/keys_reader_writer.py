from keys_path_reader import *

def read_AES_Key():
    with open(get_AES_Key_path(), 'rb') as file:
        loaded_symmetric_key = file.read()
    return loaded_symmetric_key

def read_Private_Key_Key():
    with open(get_Private_Key_path(), 'r') as file:
        loaded_private_key = file.read()
    return loaded_private_key

def read_Public_Key_Key():
    with open(get_Public_Key_path(), 'r') as file:
        loaded_public_key = file.read()
    return loaded_public_key

def write_AES_Key(data):
    with open(get_AES_Key_path(), 'wb') as file:
        file.write(data)

def write_Private_Key_Key(data):
    with open(get_Private_Key_path(), 'w') as file:
        file.write(data)

def write_Public_Key_Key(data):
    with open(get_Public_Key_path(), 'w') as file:
        file.write(data)

def write_jwks(data):
    with open(get_jwks_path(), 'w') as file:
        file.write(data)