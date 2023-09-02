

"http://127.0.0.1:5002/login";



from flask import Flask, request
from flask_cors import CORS

import json

from datetime import datetime, timedelta, timezone
from jwt.utils import get_int_from_datetime

from scripts.encode import getEncodedPayload
from scripts.decode import decode_token





myEndPoint = Flask(__name__)
cors = CORS(myEndPoint)




@myEndPoint.route("/test", methods = ['GET'])
def test():
    return {"status": "Service Up!"}, 200




@myEndPoint.route("/login", methods = ['POST'])
def login():    #of course this is only a test :)
    json_data = request.get_json()
    if (json_data['username'] == "marco.campominosi" and json_data['password'] == "enjoy"):
        test_payload = {
                            'iss': 'https://www.cm-innovationlab.it:5002',
                            'sub': 'encryptionTest',
                            'iat': get_int_from_datetime(datetime.now(timezone.utc)),
                            'exp': get_int_from_datetime(datetime.now(timezone.utc) + timedelta(minutes=30)),
                            'username': 'marco.campominosi',
                            'admin': True
                        }
        return {"content": getEncodedPayload(test_payload)}, 200
    return {"error": "Login Error!"}, 401








'''

#Get token
token = getEncodedPayload(test_payload)
print("Token:\n" + token + "\n")

#Decode token with LOCAL PUB FILE
print("Decoded token with LOCAL PUB FILE:\n" + str(decode_token(token)) + "\n")

#Decode token with WEB PUB FILE
print("Decoded token with WEB PUB FILE:\n" + str(decode_token(token, 1)) + "\n")

#Decode token with WEB JWKS
print("Decoded token with WEB JWKS:\n" + str(decode_token(token, 2)) + "\n")
















@myEndPoint.route("/api/v2/img/inference", methods = ['POST'])
def predict_image():


    # Check if the post request has the file part
    if 'userImage' not in request.files:
        return {"error": "NO FILE"}, 415

    # Get image
    img = request.files['userImage']
    img.save("inputImage")

    # Perform inference
    yoloPrediction = model("inputImage")

    # Parse results
    predictions = yoloPrediction.pred[0]
    # boxes = predictions[:, :4] # x1, y1, x2, y2
    scores = predictions[:, 4]
    categories = predictions[:, 5]

    #Dictionary for categories found
    outputDictionary = {}

    #Analysis of predictions
    for index, cat in enumerate(categories):
        type = ""
        
        if 0. in cat:
            type = "Ape"                                #red
        if 1. in cat:
            type = "Vespa"                              #pink
        if 2. in cat:
            type = "Calabrone Europeo"                  #orange
        if 3. in cat:
            type = "Vespa Orientale"                    #light orange
        if 4. in cat:
            type = "Velutina (Calabrone Asiatico)"      #yellow

        outputDictionary[str(index)] = type + "_" + str(scores[index])[7:14]   

    #yoloPrediction.show()

    image_file = 'inputImage.jpg'
    # Save results
    yoloPrediction.save(image_file)

    #Bytes convertion
    with open("runs/detect/exp/" + image_file, "rb") as f:
        im_bytes = f.read()        
    im_b64 = base64.b64encode(im_bytes).decode("utf8")



    return json.dumps({'analysis': outputDictionary, 'image': im_b64}), 200

print('App loaded!')

'''