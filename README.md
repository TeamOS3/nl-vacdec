NL-VACDEC - Decode Dutch Green Card as QR code
==============================================

Requirements
------------
* Python3
* PIL toolkit: sudo apt install python3-pilkit
* pyzbar: pip3 install pyzbar
* asn1tools: pip3 install asn1tools 
* (possibly also needed: pip3 install -U prompt-toolkit)

Decoding the QR
---------------
- Save your QR code as .png
- Run: python3 decode.py qr.png
- Or:
- First extract QR code using zbarimg: zbarimg Screenshot.png > qr.zbar
- Then: python3 decode.py qr.zbar

The Dutch try to preserve the privacy of the tested person, 
by disclosing only a small amount of information. See

* https://github.com/minvws/nl-covid19-coronacheck-app-coordination/blob/main/architecture/Privacy%20Preserving%20Green%20Card.md
* https://github.com/minvws/nl-covid19-coronacheck-app-coordination/tree/main/architecture/identity

The first attribute contains the credentialVersion and issuerPkId. The latter appears to be 'VWS-CC-n' 
where n is 1..3. Extrapolating from `https://github.com/minvws/nl-covid19-coronacheck-mobile-core/blob/main/testdata/get.sh` the actual public keys are downloaded from https://verifier-api.coronacheck.nl/v4/verifier/public_keys which is a signed JSON datastructure. The signing process is TBD. The signed JSON itself contains a BASE64 encoded JSON data structure. Use
```
curl -s https://verifier-api.coronacheck.nl/v4/verifier/public_keys | jq -r .payload | base64 -d | jq
```

The behaviour of the app also appears to be controlled from this verified-api site: 
```
curl -s https://verifier-api.coronacheck.nl/v4/verifier/config | jq -r .payload | base64 -d | jq 
```
E.g. it shows how long QR codes are valid, what vaccines are accepted, etc.

The `https://verifier-api.coronacheck.nl/` TLS certificate is signed by KPN PKIoverheid Server CA 2020
belonging to KPN B.V., which itself is certified by Staat der Nederlanden Domein Server CA 2020


Contributors
------------
- Arno Bakker  - arno481
- Karst Koymans 
- Jaap van Ginkel
- Vincent Breider

Based on original work by Hanno Boeck: https://github.com/hannob/vacdec
