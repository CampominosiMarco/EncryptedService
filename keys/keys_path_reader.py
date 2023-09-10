import os
import sys

this_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(this_script_dir)        #This is necessary to call 'properties_reader' when this scriptis imported in other folder

from properties_reader import *
        
def get_AES_Key_path():
    return os.path.join(this_script_dir, getValueFromProp('AES_Key_Name') + '.bin')

def get_Private_Key_path():
    return os.path.join(this_script_dir, getValueFromProp('Private_Key_Name') + '.pem')

def get_Public_Key_path():
    return os.path.join(this_script_dir, getValueFromProp('Public_Key_Name') + '.pub')

def get_jwks_path():
    return os.path.join(this_script_dir, "jwks.json")