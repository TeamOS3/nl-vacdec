#!/usr/bin/python3
#
# Decode the Dutch Green Pass QR code
#
# based on
#     https://github.com/hannob/vacdec
# 
# And the publicly available information from
#      https://github.com/minvws
#
# Author: Arno Bakker, Hanno Boeck, "confiks", and other cited sources
#
import sys
import PIL.Image
import pyzbar.pyzbar
import confiksbase45
import asn1tools

# From: https://github.com/minvws/nl-covid19-coronacheck-idemix/blob/main/common/common.go#L35
# Attributes start with a CredentialMetadata spec, then the
# attributes from AttributeTypesV2 list
#     https://github.com/minvws/nl-covid19-coronacheck-idemix/blob/main/verifier/verifier.go#L180
#
AttributeTypesV2 = [
    "CredentialMetadata",
    "isSpecimen",
    "isPaperProof",
    "validFrom",
    "validForHours",
    "firstNameInitial",
    "lastNameInitial",
    "birthDay",
    "birthMonth"
]


if len(sys.argv) != 2:
    print("Usage: decode.py qr.{png,jpg}")
    print("or")
    print("zbarimg screenshot.{png,jpg} > qr.txt")
    print("and: decode.py qr.txt")
    sys.exit(-1)

if sys.argv[1].endswith(".png") or sys.argv[1].endswith(".jpg"):
    img = PIL.Image.open(sys.argv[1])
    qrdata = pyzbar.pyzbar.decode(img)
    proofdata = qrdata[0].data
else:
    f = open(sys.argv[1],"rb")
    zbardata = f.read()
    f.close()
    proofdata = zbardata[len("QR-Code:"):]
    
# See https://github.com/minvws/nl-covid19-coronacheck-idemix/blob/main/verifier/verifier.go#L29

# Header: 'NL' + proofVersionByte + proofBase45

if str(chr(proofdata[2])) != '2':
    print("Not a version 2 proof")
    sys.exit(-1)
    
# Skip NL2: as per Hanno  (3: gives ASN parse error)
b45data = proofdata[4:]

# Dutch do not use IETF BASE45, but some variant, as documented:
#  https://news.ycombinator.com/item?id=27628178    
#  https://gist.github.com/confiks/8fcb480d87a50cf1bb5e40e2f0930fad
# 
asn1data = confiksbase45.b58decode(b45data)

parser = asn1tools.compile_files("nl-domestic.asn1")

d = parser.decode('ProofSerV2',asn1data)

#print(d)

ad = d['aDisclosed']

for i in range(0,len(ad)):
    val = ad[i]
    
    # Actual values are right-shifted 1: 
    # https://github.com/minvws/nl-covid19-coronacheck-idemix/blob/main/common/common.go#L137
    dec = val >> 1;
    
    if i == 0:
        # CredentialMetadata
        # This integer is another ASN.1 sequence. So convert to bytes,
        # and parse. The number 15 comes from asn1parse
        cm = dec.to_bytes(15,byteorder='big')
        d2 = parser.decode('CredentialMetadataSer',cm)
        
        # Public keys listed in
        # nl-covid19-coronacheck-mobile-core/testdata/public_keys.json
	#
        # Sample data showed VWS-CC-1 or VWS-CC-2 as Issuer
        print("Decoded CredentialMetadata",d2)

        continue
    
    if dec < 256:
        c = chr(dec)
    else:
    	c = '?'
    print("Decoded",AttributeTypesV2[i],dec,c)
