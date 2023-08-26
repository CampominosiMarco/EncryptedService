from jproperties import Properties

def getValue(key, file = 'properties.properties'):
    
    current_properties = Properties()
    with open(file, 'rb') as read_prop:
        current_properties.load(read_prop)
        
    prop_view = current_properties.items()

    for item in prop_view:
    #    print('KEY: ' + item[0], ' VALUE: ', item[1].data)
        if (item[0] == key):
            return item[1].data