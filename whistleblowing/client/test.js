const crypto = require('crypto');
const NodeRSA = require('node-rsa');

// 1. Genera una chiave RSA per la firma digitale
const privateKey = new NodeRSA({ b: 2048 }); // Genera una chiave privata RSA di 2048 bit
const publicKey = privateKey.exportKey('pkcs1-public'); // Estrai la chiave pubblica RSA

// 2. Cifra l'username e la password con una chiave simmetrica (AES)
const symmetricKey = crypto.randomBytes(32); // Genera una chiave simmetrica AES





const fs = require('fs');

// Salva la chiave AES in un file crittografato
const keyData = symmetricKey.toString('base64');
fs.writeFileSync('aes_key.txt', keyData, 'utf8');

// Per leggere la chiave AES in seguito:
const loadedKeyData = fs.readFileSync('aes_key.txt', 'utf8');
const loadedSymmetricKey = Buffer.from(loadedKeyData, 'base64');













const username = 'pino';
const password = 'strampalato';
const userData = { username, password };
const jsonText = JSON.stringify(userData);

console.log('\nuserData:', userData, ' - jsonText:', jsonText);


const iv = crypto.randomBytes(16); // Genera un vettore di inizializzazione (IV) casuale
const cipher = crypto.createCipheriv('aes-256-cbc', symmetricKey, iv);

// Salva l'IV insieme ai dati cifrati
let encryptedData = iv.toString('base64') + cipher.update(jsonText, 'utf8', 'base64');          //aggiunto           iv.toString('base64')

encryptedData += cipher.final('base64');









// 3. Firma digitalmente il JSON cifrato con la chiave privata RSA
const signature = privateKey.sign(encryptedData, 'base64', 'base64');

// Ora hai il JSON cifrato, la firma digitale e la chiave pubblica RSA per la verifica
console.log('\nIV:', iv.toString('base64'));
console.log('\nIV concat a JSON cifrato:', encryptedData);
console.log('\nFirma digitale:', signature);
console.log('\nChiave pubblica RSA:', publicKey);

// Per verificare la firma digitale con la chiave pubblica RSA
const publicKeyVerify = new NodeRSA(publicKey, 'pkcs1-public');
const isVerified = publicKeyVerify.verify(encryptedData, signature, 'base64', 'base64');






if (isVerified) {
    console.log('\nLa firma è verificata!');
  // 2. La firma è valida, ora puoi decifrare i dati cifrati con la chiave simmetrica AES


  const ivDecryption = Buffer.from(encryptedData.slice(0, 24), 'base64');
  const encryptedText = Buffer.from(encryptedData.slice(24), 'base64');



  const decipher = crypto.createDecipheriv('aes-256-cbc', symmetricKey, ivDecryption);
  let decryptedData = decipher.update(encryptedText, 'binary', 'utf8');
  decryptedData += decipher.final('utf8');








  // 3. Hai ora il JSON originale
  const originalData = JSON.parse(decryptedData);

  console.log('\nDati originali:', originalData);
} else {
  console.log('\nFirma non valida. I dati potrebbero essere stati alterati.');
}





