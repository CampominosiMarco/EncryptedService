# EncryptedService
A way to encrypt your service...

## Let's see the KEYS (see 'keys' folder)
First of all, starting from GitHub [python-encrypted-rsa-keys-demo](https://github.com/Aaron-K-T-Berry/python-encrypted-rsa-keys-demo) project, we create pair keys for encryption.<br/>
Read also [Aaron-K-T-Berry tutorial on dev.to](https://dev.to/aaronktberry/generating-encrypted-key-pairs-in-python-69b).<br/>
The original source code was modified to read informations from a 'properties' file like JAVA.
* `pip install jproperties`
* Please read [pypi.org: jproperties](https://pypi.org/project/jproperties/)
* Please read [geeksforgeeks.org: jproperties example](https://www.geeksforgeeks.org/read-properties-file-using-jproperties-in-python/)

Run python script:
```bash
py -3 .\keys_generator.py
```


## JWT
Wiki [https://en.wikipedia.org/wiki/JSON_Web_Token](https://en.wikipedia.org/wiki/JSON_Web_Token)

In a public-key encryption system, anyone with a public key can encrypt a message, yielding a ciphertext, but only those who know the corresponding private key can decrypt the ciphertext to obtain the original message.

[https://jwt.io/](https://jwt.io/)

`pip install jwt`
[https://pypi.org/project/jwt/](https://pypi.org/project/jwt/)


https://datatracker.ietf.org/doc/html/rfc7517
JSON Web Key Sets
he JSON Web Key Set (JWKS) is a set of keys containing the public keys used to verify any JSON Web Token (JWT) issued by the Authorization Server and signed using the RS256

https://medium.com/geekculture/how-to-encode-and-decode-jwt-token-using-python-f9c33de576c5



per leggere jwks json
pip install httpx


https://pypi.org/project/requests-jwt/


# whistleblowing
#creare anche una chiave pubblica per chi mi vuole scrivere mess criptati