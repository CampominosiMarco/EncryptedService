

// Genera un vettore di inizializzazione (IV) casuale di 16 byte
const iv = window.crypto.getRandomValues(new Uint8Array(16));



let my_JWT

function sendPostRequest(){
    let myLoginJSON = {username: "marco.campominosi", password: "enjoy"};

    document.getElementById("thirdField").setAttribute("hidden", "");
    document.getElementById("fourthField").setAttribute("hidden", "");
            
    var xhttp = new XMLHttpRequest();
    var url = "http://127.0.0.1:5002/login";
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            const obj = JSON.parse(this.responseText);

            my_JWT = obj.content.token;

            visibleCode = "<br/>"
            splitted = obj.content.token.match(/.{1,50}/g) ?? [];

            for (i = 0; i < splitted.length; i++) {
                visibleCode += "&emsp;&emsp;&emsp;&emsp;" + splitted[i] + "<br/>";
            }

            divOutput = "{<br/>&emsp;iss: " + obj.content.iss + ",<br/>" + 
                "&emsp;iat: " + obj.content.iat + ",<br/>" + 
                "&emsp;exp: " + obj.content.exp + ",<br/>" + 
                "&emsp;sub: " + obj.content.sub + ",<br/>" + 
                "&emsp;token: " + visibleCode + "}"
                        


            document.getElementById("secondDiv").innerHTML = divOutput;
            document.getElementById("secondField").removeAttribute("hidden");
            document.getElementById("thirdField").removeAttribute("hidden");

            myAESEncrypt(myJSONMessage);


        }
    }
    xhttp.open("POST", url);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.send(JSON.stringify(myLoginJSON));  //JSON.stringify(myLoginJSON)
}



let myJSONMessage = {message: "This is a test!"};

let returnEncrypted = {};


function sendRequestWithJWT(){
    

    document.getElementById("fourthField").setAttribute("hidden", "");
            
    var xhttp = new XMLHttpRequest();
    var url = "http://127.0.0.1:5002/message_receiver";
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            const obj = JSON.parse(this.responseText);

            document.getElementById("fourthDiv").innerHTML = obj.array_resp;
            document.getElementById("fourthField").removeAttribute("hidden");
        }
    }
    xhttp.open("POST", url);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.setRequestHeader('Authorization', 'Bearer ' + my_JWT);


//encrypt 

    xhttp.send(JSON.stringify(returnEncrypted));

}





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


let cryptoKey

// https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/importKey

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
                cryptoKey = promiseKey;
            })
        })
    .catch((e) => console.error("importPublicKey: " + e));


let loadedSymmetricKey
 
fetch('../../keys/cm-innovationlab.it_aes.bin')
    .then((res) =>   res.text())
    .then((text ) => {
        crypto.subtle.importKey(
            "raw",
            keyAESToArrayBuffer(text),
            {
                //hash: "SHA-256",
                //length: 256
                name: 'AES-CBC'
            },
            false,
            ["encrypt", "decrypt"]
            )
            .then((promiseKey) => {
                loadedSymmetricKey = promiseKey;
            })
        })
    .catch((e) => console.error("importAESKey: " + e));



function myRSAEncrypt(jsonMsg){
    window.crypto.subtle.encrypt(
        {
            name: "RSA-OAEP"
        },
        cryptoKey,
        new TextEncoder().encode(jsonMsg)
        )
        .then((res) =>{
            var byteArray = new Uint8Array(res);
            document.getElementById("thirdDiv").innerHTML = byteArray;
            returnEncrypted = {"array": byteArray};
        })
    .catch((e) => console.error("myRSAEncrypt: " + e));
}

function myAESEncrypt(jsonMsg){
    window.crypto.subtle.encrypt(
        {
            name: "AES-CBC"
        },
        loadedSymmetricKey,
        new TextEncoder().encode(jsonMsg)
        )
        .then((res) =>{
            var byteArray = new Uint8Array(res);
            document.getElementById("thirdDiv").innerHTML = byteArray;
            returnEncrypted = {"array": byteArray};
        })
    .catch((e) => console.error("myAESEncrypt: " + e));
}
