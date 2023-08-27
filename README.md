# EncryptedService
A way to encrypt your service...

If you are new of cryptography read something on [wikipedia.org: Public-key cryptography](https://en.wikipedia.org/wiki/Public-key_cryptography) but we can resume: "In a public-key encryption system, anyone with a public key can encrypt a message, yielding a ciphertext, but only those who know the corresponding private key can decrypt the ciphertext to obtain the original message" and viceversa.

This [image about 'RS256 asymmetric algorithm'](https://global.discourse-cdn.com/auth0/original/3X/7/0/709aa9a1d6e7fb8944e525e956a34bb0d63554d7.png) explain easily what I try to obtain with this project:<br/>
![RS256 asymmetric algorithm](https://global.discourse-cdn.com/auth0/original/3X/7/0/709aa9a1d6e7fb8944e525e956a34bb0d63554d7.png)

## Let's see the KEYS (see 'keys' folder)
First of all, starting from GitHub project [python-encrypted-rsa-keys-demo](https://github.com/Aaron-K-T-Berry/python-encrypted-rsa-keys-demo), I created pair keys for encryption.<br/>
* Read [cryptography.io DOCS](https://cryptography.io/en/latest/).<br/>
* Read also [Aaron-K-T-Berry tutorial on dev.to](https://dev.to/aaronktberry/generating-encrypted-key-pairs-in-python-69b).
  
The original source code was modified to read informations from a 'properties' file like JAVA.
* `pip install jproperties`
* Please read [pypi.org: jproperties](https://pypi.org/project/jproperties/)
* Please read [geeksforgeeks.org: jproperties example](https://www.geeksforgeeks.org/read-properties-file-using-jproperties-in-python/)

Also I added JSON Web Key Sets (JWKS) creation to verify JSON Web Token (JWT).
* Please read [Request for Comments: 7517](https://datatracker.ietf.org/doc/html/rfc7517)

Run python script from 'keys' folder:
```bash
py -3 .\keys_generator.py
```
## JWT (encode & decode scripts)
Ok, now we have the keys. But what is JSON Web Token (JWT)? <br/>
* Read [wikipedia.org: JWT](https://en.wikipedia.org/wiki/JSON_Web_Token)
* Also visit this amazing page [jwt.io](https://jwt.io/)

First of all python jwt project is needed, so install it:information and verify signature.
* `pip install jwt`
* Read more on [pypi.org: jwt](https://pypi.org/project/jwt/)

You can find three simple scripts:
* First one is "encode.py" to obtain a token
* The second is "decode.py" which gives 3 possible ways to decode token (with or without verification):
  1. Decode token with <u>LOCAL PUB FILE</u>
  2. Decode token with <u>WEB PUB FILE</u>
  3. Decode token with <u>WEB JWKS</u>
* The last is "test_enc_dec.py" for testing
  
Run python script:
```bash
py -3 .\test_enc_dec.py
```
# Whistleblowing
Now let's try to help who need to encrypt information or verify signature with some real cases.<br/>



flask --app endPoint run --host=0.0.0.0 --port 5002



https://pypi.org/project/requests-jwt/