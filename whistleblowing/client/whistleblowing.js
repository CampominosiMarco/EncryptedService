
let my_JWT

function sendPostRequest(){
    let myJSON = {username: "marco.campominosi", password: "enjoy"};

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
        }
    }
    xhttp.open("POST", url);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.send(JSON.stringify(myJSON));
}








function sendRequestWithJWT(){
    let myJSON = {message: "This is a test!"};

    document.getElementById("fourthField").setAttribute("hidden", "");
            
    var xhttp = new XMLHttpRequest();
    var url = "http://127.0.0.1:5002/message_receiver";
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            const obj = JSON.parse(this.responseText);

            document.getElementById("thirdDiv").innerHTML = obj.content;
            document.getElementById("thirdField").removeAttribute("hidden");
            document.getElementById("fourthField").removeAttribute("hidden");
        }
    }
    xhttp.open("POST", url);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.setRequestHeader('Authorization', 'Bearer ' + my_JWT);


//encrypt with public key

    xhttp.send(JSON.stringify(myJSON));

}




















function removeLines(str) {
    return str.replace("\n", "");
}

function base64ToArrayBuffer(b64) {
    var byteString = window.atob(b64);
    var byteArray = new Uint8Array(byteString.length);
    for(var i=0; i < byteString.length; i++) {
        byteArray[i] = byteString.charCodeAt(i);
    }

    return byteArray;
}

function pemToArrayBuffer(pem) {
    var b64Lines = removeLines(pem);
    var b64Prefix = b64Lines.replace('-----BEGIN PUBLIC KEY-----', '');
    var b64Final = b64Prefix.replace('-----END PUBLIC KEY-----', '');

    return base64ToArrayBuffer(b64Final);
}







let pemEncodedKey

fetch("../server/scripts/keys/cm-innovationlab.it_public_.pub")
  .then((res) => res.text())
  .then((text) => {
    pemEncodedKey = text

   // console.log(pemEncodedKey)


   publicKey = window.crypto.subtle.importKey(
        "pkcs8",
        pemToArrayBuffer(pemEncodedKey),
        {
            name: "RSA-OAEP",
            hash: {name: "SHA-256"}
        },
        true,
        ["encrypt", "decrypt"]
    );



   })
  .catch((e) => console.error(e));

//const reader = new FileReader();

//const pemEncodedKey = reader.readAsDataURL("../server/scripts/keys/cm-innovationlab.it_public_.pub");

//console.log(pemEncodedKey)

/*publicKey = window.crypto.subtle.importKey(pemEncodedKey)


console.log(publicKey)


//let publicKey = await importKey(pemEncodedKey);

const encryptedData = window.crypto.subtle.encrypt(
    {
      name: "RSA",
    },
    publicKey, // from generateKey or importKey above
    {"data": "ciao"} // ArrayBuffer of data you want to encrypt
  );*/


