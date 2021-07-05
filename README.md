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
by disclosing only a small amount of information in the form of attributes. See

* https://github.com/minvws/nl-covid19-coronacheck-app-coordination/blob/main/architecture/Privacy%20Preserving%20Green%20Card.md
* https://github.com/minvws/nl-covid19-coronacheck-app-coordination/tree/main/architecture/identity


Keys Used
---------
The first attribute contains the credentialVersion and issuerPkId. The latter appears to be 'VWS-CC-n' 
where n is 1..3. Extrapolating from `https://github.com/minvws/nl-covid19-coronacheck-mobile-core/blob/main/testdata/get.sh` the actual public keys are downloaded from https://verifier-api.coronacheck.nl/v4/verifier/public_keys which is a signed JSON datastructure. The signing process is TBD. The signed JSON itself contains a BASE64 encoded JSON data structure. Use
```
curl -s https://verifier-api.coronacheck.nl/v4/verifier/public_keys | jq -r .payload | base64 -d | jq
```
The `public_key` field in this JSON data structure contains a BASE64 encoded XML file, e.g. for VWS-CC-1:
```
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<IssuerPublicKey xmlns="http://www.zurich.ibm.com/security/idemix">
   <Counter>0</Counter>
   <ExpiryDate>1646817725</ExpiryDate>
   <Elements>
      <n>...</n>
      <Z>...</Z>
      <S>...</S>
      <G>...</G>
      <H>...</H>
      <Bases num="12">
         <Base_0>...</Base_0>
         <Base_1>
...
         </Base_11>
      </Bases>
   </Elements>
   <Features>
      <Epoch length="432000"></Epoch>
   </Features>
   <ECDSA>MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE07Z7i2/6nHw+E8H7b5vSLNdpRd20WwLjlwhc0QEeebfvR8TCVPVM0Yetu8Ecl+KSDc1FvWUuRUNWQvbtUSNNkg==</ECDSA>
```

This again points to the use of IBM Zurich's IDEMIX crypto system ([paper](https://www.zurich.ibm.com/pdf/csc/Identity_Mixer_Nov_2015.pdf),[site](https://www.zurich.ibm.com/idemix)). When we look at the [actual verification code](https://github.com/minvws/nl-covid19-coronacheck-idemix/blob/main/verifier/verifier.go), the keys are used
as input to [GABI](https://github.com/privacybydesign/gabi), "a Go implementation of the IRMA approach to the Idemix attribute based credential system."


Miscellaneous
-------------
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
