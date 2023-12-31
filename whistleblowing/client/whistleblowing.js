/********************************************************************************************
GLOBAL VARIABLES
********************************************************************************************/

let myLoginJSON = {username: "marco.campominosi", password: "enjoy"};
let myJSONMessage = {message: "This is a test!"};
let my_JWT
let rsaPublicCriptoKey
let aesCriptoKey
let encryptedData = {};

/********************************************************************************************
KEYS READER
********************************************************************************************/

function base64ToArrayBuffer(b64) {
    var byteString = window.atob(b64);
    const bufferArray = new ArrayBuffer(byteString.length);
    var byteArray = new Uint8Array(bufferArray);
    for(var i=0; i < byteString.length; i++) {
        byteArray[i] = byteString.charCodeAt(i);
    }

    return byteArray;
}

function keyRSAToArrayBuffer(key) {
    var b64Final = key.replace(/(?:\r\n|\r|\n)/g, "")
                        .replace('-----BEGIN PUBLIC KEY-----', '')
                        .replace('-----END PUBLIC KEY-----', '');

    return base64ToArrayBuffer(b64Final);
}

function keyAESToArrayBuffer(key) {
    var b64Final = key.replace(/-/g, '+').replace(/_/g, '/');

    return base64ToArrayBuffer(b64Final);
}

function fromByteArrayToString(byteArray){
    return btoa(String.fromCharCode.apply(null, byteArray));
}

//Importing Public key and AES key  [https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/importKey]

fetch("../../keys/cm-innovationlab.it_public.pub")
    .then((res) => res.text())
    .then((text) => {
        window.crypto.subtle.importKey(
            "spki",
            keyRSAToArrayBuffer(text),
            {
                name: "RSA-OAEP",
                hash: "SHA-256"
            },
            true,
            ["encrypt"]
            )
            .then((promiseKey) => {
                rsaPublicCriptoKey = promiseKey;
            })
        })
    .catch((e) => console.error("importPublicKey:\n" + e));


fetch('../../keys/cm-innovationlab.it_aes.bin')
    .then((res) =>   res.text())
    .then((text) => {
        window.crypto.subtle.importKey(
            "raw",
            keyAESToArrayBuffer(text),
            {
                hash: "SHA-256",
                length: 256,
                name: 'AES-CBC'
            },
            false,
            ["encrypt", "decrypt"]
            )
            .then((promiseKey) => {
                aesCriptoKey = promiseKey;
                myAESEncrypt(myLoginJSON, "firstDiv");
            })
        })
    .catch((e) => console.error("importAESKey:\n" + e));

/********************************************************************************************
ENCRYPTION
********************************************************************************************/

//unused
function myRSAEncrypt(jsonMsg, destination){
    window.crypto.subtle.encrypt(
        {
            name: "RSA-OAEP"
        },
        rsaPublicCriptoKey,
        new TextEncoder().encode(JSON.stringify(jsonMsg))
        )
        .then((res) =>{
            var byteArray = new Uint8Array(res);
            var byteArrayString = fromByteArrayToString(byteArray);
            document.getElementById(destination).innerHTML = splitLongString(byteArrayString, 0);
            encryptedData = {"byte_array": byteArray};
        })
    .catch((e) => console.error("myRSAEncrypt: " + e));
}

function myAESEncrypt(jsonMsg, destination){

    const iv = window.crypto.getRandomValues(new Uint8Array(16))

    window.crypto.subtle.encrypt(
        {
            name: "AES-CBC",
            iv: iv
        },
        aesCriptoKey,
        new TextEncoder().encode(JSON.stringify(jsonMsg))
        )
        .then((res) =>{
            var byteArray = new Uint8Array(res);
            var byteArrayString = fromByteArrayToString(byteArray);
            document.getElementById(destination).innerHTML = splitLongString(byteArrayString, 0);
            encryptedData = {"byte_array": byteArray, "iv": iv};
        })
    .catch((e) => console.error("myAESEncrypt: " + e));
}

/********************************************************************************************
POST REQUESTS
********************************************************************************************/

function sendPostRequest(){

    document.getElementById("thirdField").setAttribute("hidden", "");
    document.getElementById("fourthField").setAttribute("hidden", "");
            
    var xhttp = new XMLHttpRequest();
    var url = "https://www.cm-innovationlab.it:5002/login";
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            const obj = JSON.parse(this.responseText);

            if ("error" in obj) {
                document.getElementById("secondDiv").innerHTML = obj.error;
            } else {
                my_JWT = obj.content.token;

                divOutput = "{<br/>&emsp;iss: " + obj.content.iss + ",<br/>" + 
                //    "&emsp;iat: " + obj.content.iat + ",<br/>" + 
                //    "&emsp;exp: " + obj.content.exp + ",<br/>" + 
                    "&emsp;sub: " + obj.content.sub + ",<br/>" + 
                    "&emsp;token: " + splitLongString(obj.content.token, 4) + "}"
    
                document.getElementById("secondDiv").innerHTML = divOutput;
                document.getElementById("secondField").removeAttribute("hidden");
                document.getElementById("thirdField").removeAttribute("hidden");
    
                myAESEncrypt(myJSONMessage, "thirdDiv");
            }
        }
    }
    xhttp.open("POST", url);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.send(JSON.stringify(encryptedData));
}

function sendRequestWithJWT(){
    
    document.getElementById("fourthField").setAttribute("hidden", "");
            
    var xhttp = new XMLHttpRequest();
    var url = "https://www.cm-innovationlab.it:5002/message_receiver";
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            const obj = JSON.parse(this.responseText);

            if ("error" in obj) {
                document.getElementById("fourthDiv").innerHTML = obj.error;
            } else {
                document.getElementById("fourthDiv").innerHTML = 
                "&#9194; <b><span style='color:green'>Reverse message from server side: </span></b>" + obj.content + "<br/>" +
                "&#11088; <b><span style='color:green'>Token request owner: </span></b>" + obj.request_owner + "<br/>" +
                "&#8987; <b><span style='color:green'>Token remaining time: </span></b>" + obj.remaining_time + " minutes";
                document.getElementById("fourthField").removeAttribute("hidden");
            }
        }
    }
    xhttp.open("POST", url);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.setRequestHeader('Authorization', 'Bearer ' + my_JWT);
    xhttp.send(JSON.stringify(encryptedData));
}

/********************************************************************************************
EXTRA
********************************************************************************************/

function splitLongString(inputString, tabs){
    visibleCode = "<br/>"
    splitted = inputString.match(/.{1,50}/g) ?? [];

    for (i = 0; i < splitted.length; i++) {
        for (t = 0; t < tabs; t++){
            visibleCode += "&emsp;"
        }
        visibleCode += splitted[i] + "<br/>";
    }
    return visibleCode;
}