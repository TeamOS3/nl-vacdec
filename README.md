NL-VACDEC - Decode Dutch Green Card as QR code
==============================================

Requirements
------------
* Python3
* PIL toolkit: sudo apt install python3-pilkit
* pyzbar:  pip3 install pyzbar
* asn1tools: pip3 install asn1tools 

Getting started
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

Contributors
------------
- Arno Bakker  - arno481
- Karst Koymans 
- Jaap van Ginkel
- Vincent Breider

Based on original work by Hanno Boeck: https://github.com/hannob/vacdec