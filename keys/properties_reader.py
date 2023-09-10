from jproperties import Properties
import os

file_name = 'properties.properties'
this_script_dir = os.path.dirname(os.path.abspath(__file__))    #Absolute Path of current script
file_path = os.path.join(this_script_dir, file_name)            #Relative Path of file

def getValueFromProp(key, file = file_path):
    
    current_properties = Properties()
    with open(file, 'rb') as read_prop:
        current_properties.load(read_prop)
        
    prop_view = current_properties.items()

    for item in prop_view:
    #    print('KEY: ' + item[0], ' VALUE: ', item[1].data)
        if (item[0] == key):
            return item[1].data