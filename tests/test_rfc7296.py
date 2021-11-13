#
# This file is part of pyasn1-modules software.
#
# Created by Russ Housley
# Copyright (c) 2019, Vigil Security, LLC
# License: http://snmplabs.com/pyasn1/license.html
#
import sys
import unittest

from pyasn1.codec.der.decoder import decode as der_decoder
from pyasn1.codec.der.encoder import encode as der_encoder

from pyasn1_modules import pem, rfc7296


class CertBundleTestCase(unittest.TestCase):
    cert_bundle_pem_text = """\
MIITfqCCA8kwggPFMIICraADAgECAhACrFwmagtAm48LefKuRiV3MA0GCSqGSIb3
DQEBBQUAMGwxCzAJBgNVBAYTAlVTMRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMxGTAX
BgNVBAsTEHd3dy5kaWdpY2VydC5jb20xKzApBgNVBAMTIkRpZ2lDZXJ0IEhpZ2gg
QXNzdXJhbmNlIEVWIFJvb3QgQ0EwHhcNMDYxMTEwMDAwMDAwWhcNMzExMTEwMDAw
MDAwWjBsMQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYD
VQQLExB3d3cuZGlnaWNlcnQuY29tMSswKQYDVQQDEyJEaWdpQ2VydCBIaWdoIEFz
c3VyYW5jZSBFViBSb290IENBMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKC
AQEAxszlc+b71LvlLS0ypt/lgT/JzSVJtnEqw9WUNGeiChywX2mmQLHEt7KP0Jik
qUFZOtPclNY823Q4pErMTSWC90qlUxI47vNJbXGRfmO2q6Zfw6SE+E9iUb74xezb
OJLjBuUIkQzEKEFV+8taiRV+ceg1v01yCT2+OjhQW3cxG42zxyRFmqesbQAUWgS3
uhPrUQqYQUEiTmVhh4FBUKZ5XIneGUpX1S7mXRxTLH6YzRoGFqRoc9A0BBNcoXHT
WnxV215k4TeHMFYE5RG0KYAS8Xk5iKICEXwnZreIt3jyygqoOKsKZMK/Zl2VhMGh
JR6HXRpQCyASzEG7bgtROLhLywIDAQABo2MwYTAOBgNVHQ8BAf8EBAMCAYYwDwYD
VR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQUsT7DaQP4v0cB1JgmGggC72NkK8MwHwYD
VR0jBBgwFoAUsT7DaQP4v0cB1JgmGggC72NkK8MwDQYJKoZIhvcNAQEFBQADggEB
ABwaBpfc15yfPIhmBghXIdshR/gqZ6q/GDJ2QBBXwYrzetkRZY41+p78RbWe2Uwx
S7iR6EMsjrN4ztvjU3lx1uUhlAHaVYeaJGT2imbM3pw3zag0sWmbI8ieeCIrcEPj
VUcxYRnvWMWFL04w9qAxFiPI5+JlFjPLvxoboD34yl6LMYtgCIktDAZcUrfE+QqY
0RVfnxK+fDZjOL1EpH/kJisKxJdpDemM4sAQV7jIdhKRVfJIadi8KgJbD0TUIDHb
9LpwJl2QYJ68SxcJL7TLHkNoyQcnwdJc9+ohuWgSnDycv578gFybY83sR6olJ2eg
N/MAgn1U16n46S4To3foH0qgggS6MIIEtjCCA56gAwIBAgIQDHmpRLCMEZUgkmFf
4msdgzANBgkqhkiG9w0BAQsFADBsMQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGln
aUNlcnQgSW5jMRkwFwYDVQQLExB3d3cuZGlnaWNlcnQuY29tMSswKQYDVQQDEyJE
aWdpQ2VydCBIaWdoIEFzc3VyYW5jZSBFViBSb290IENBMB4XDTEzMTAyMjEyMDAw
MFoXDTI4MTAyMjEyMDAwMFowdTELMAkGA1UEBhMCVVMxFTATBgNVBAoTDERpZ2lD
ZXJ0IEluYzEZMBcGA1UECxMQd3d3LmRpZ2ljZXJ0LmNvbTE0MDIGA1UEAxMrRGln
aUNlcnQgU0hBMiBFeHRlbmRlZCBWYWxpZGF0aW9uIFNlcnZlciBDQTCCASIwDQYJ
KoZIhvcNAQEBBQADggEPADCCAQoCggEBANdTpARR+JmmFkhLZyeqk0nQOe0MsLAA
h/FnKIaFjI5j2ryxQDji0/XspQUYuD0+xZkXMuwYjPrxDKZkIYXLBxA0sFKIKx9o
m9KxjxKws9LniB8f7zh3VFNfgHk/LhqqqB5LKw2rt2O5Nbd9FLxZS99RStKh4gzi
kIKHaq7q12TWmFXo/a8aUGxUvBHy/Urynbt/DvTVvo4WiRJV2MBxNO723C3sxIcl
ho3YIeSwTQyJ3DkmF93215SF2AQhcJ1vb/9cuhnhRctWVyh+HA1BV6q3uCe7seT6
Ku8hI3UarS2bhjWMnHe1c63YlC3k8wyd7sFOYn4XwHGeLN7x+RAoGTMCAwEAAaOC
AUkwggFFMBIGA1UdEwEB/wQIMAYBAf8CAQAwDgYDVR0PAQH/BAQDAgGGMB0GA1Ud
JQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjA0BggrBgEFBQcBAQQoMCYwJAYIKwYB
BQUHMAGGGGh0dHA6Ly9vY3NwLmRpZ2ljZXJ0LmNvbTBLBgNVHR8ERDBCMECgPqA8
hjpodHRwOi8vY3JsNC5kaWdpY2VydC5jb20vRGlnaUNlcnRIaWdoQXNzdXJhbmNl
RVZSb290Q0EuY3JsMD0GA1UdIAQ2MDQwMgYEVR0gADAqMCgGCCsGAQUFBwIBFhxo
dHRwczovL3d3dy5kaWdpY2VydC5jb20vQ1BTMB0GA1UdDgQWBBQ901Cl1qCt7vNK
YApl0yHU+PjWDzAfBgNVHSMEGDAWgBSxPsNpA/i/RwHUmCYaCALvY2QrwzANBgkq
hkiG9w0BAQsFAAOCAQEAnbbQkIbhhgLtxaDwNBx0wY12zIYKqPBKikLWP8ipTa18
CK3mtlC4ohpNiAexKSHc59rGPCHg4xFJcKx6HQGkyhE6V6t9VypAdP3THYUYUN9X
R3WhfVUgLkc3UHKMf4Ib0mKPLQNa2sPIoc4sUqIAY+tzunHISScjl2SFnjgOrWNo
PLpSgVh5oywM395t6zHyuqB8bPEs1OG9d4Q3A84ytciagRpKkk47RpqF/oOi+Z6M
o8wNXrM9zwR4jxQUezKcxwCmXMS1oVWNWlZopCJwqjyBcdmdqEU79OX2olHdx3ti
6G8MdOu42vi/hw15UJGQmxg7kVkn8TUoE6smftX3eqCCB9wwggfYMIIGwKADAgEC
AhABW9pmX8RLdRe2iCweq9TcMA0GCSqGSIb3DQEBCwUAMHUxCzAJBgNVBAYTAlVT
MRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMxGTAXBgNVBAsTEHd3dy5kaWdpY2VydC5j
b20xNDAyBgNVBAMTK0RpZ2lDZXJ0IFNIQTIgRXh0ZW5kZWQgVmFsaWRhdGlvbiBT
ZXJ2ZXIgQ0EwHhcNMTgwODE0MDAwMDAwWhcNMjAwODE4MTIwMDAwWjCB3DEdMBsG
A1UEDwwUUHJpdmF0ZSBPcmdhbml6YXRpb24xEzARBgsrBgEEAYI3PAIBAxMCVVMx
GTAXBgsrBgEEAYI3PAIBAhMIRGVsYXdhcmUxEDAOBgNVBAUTBzMwMTQyNjcxCzAJ
BgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMREwDwYDVQQHEwhTYW4gSm9z
ZTEVMBMGA1UEChMMUGF5UGFsLCBJbmMuMRQwEgYDVQQLEwtDRE4gU3VwcG9ydDEX
MBUGA1UEAxMOd3d3LnBheXBhbC5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAw
ggEKAoIBAQDOofrgGYvXjVHH1WKEgxO51/bNk8Vw0WlZAyu0iwAUULZ3mrI8+xOw
gE5VGghgoQY9QNIA0mdFPrEmRRQAZXitszlL5s8oks4+tFzBHHtJp2D9BixRKxAR
Afo6c54tufaJUrQyIMwr2mpfbPox3palkK7RmHdimcOqtUjjQyS/WcHxMkyX3wa9
e1JoEB9ofJGupNnC90uGgxilWLvOtn/27w56p2AYkKoSGgXsNRGE5ySxns23sZOo
tgSeTRe16K7X5JuzPcGtZGMRxlkVagZsrp8rNsf4aq0wKkBjkvVzSvJTaDJSDqEt
hV+ZoGSFYpwaHArVir0sJ63E/aq2Tb97AgMBAAGjggP6MIID9jAfBgNVHSMEGDAW
gBQ901Cl1qCt7vNKYApl0yHU+PjWDzAdBgNVHQ4EFgQUuzrmqCkAmIQyec538AFt
Xwp5Y7kwgaUGA1UdEQSBnTCBmoIOd3d3LnBheXBhbC5jb22CEmhpc3RvcnkucGF5
cGFsLmNvbYIMdC5wYXlwYWwuY29tggxjLnBheXBhbC5jb22CDWM2LnBheXBhbC5j
b22CFGRldmVsb3Blci5wYXlwYWwuY29tggxwLnBheXBhbC5jb22CFXd3dy5wYXlw
YWxvYmplY3RzLmNvbYIOY21zLnBheXBhbC5jb20wDgYDVR0PAQH/BAQDAgWgMB0G
A1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjB1BgNVHR8EbjBsMDSgMqAwhi5o
dHRwOi8vY3JsMy5kaWdpY2VydC5jb20vc2hhMi1ldi1zZXJ2ZXItZzIuY3JsMDSg
MqAwhi5odHRwOi8vY3JsNC5kaWdpY2VydC5jb20vc2hhMi1ldi1zZXJ2ZXItZzIu
Y3JsMEsGA1UdIAREMEIwNwYJYIZIAYb9bAIBMCowKAYIKwYBBQUHAgEWHGh0dHBz
Oi8vd3d3LmRpZ2ljZXJ0LmNvbS9DUFMwBwYFZ4EMAQEwgYgGCCsGAQUFBwEBBHww
ejAkBggrBgEFBQcwAYYYaHR0cDovL29jc3AuZGlnaWNlcnQuY29tMFIGCCsGAQUF
BzAChkZodHRwOi8vY2FjZXJ0cy5kaWdpY2VydC5jb20vRGlnaUNlcnRTSEEyRXh0
ZW5kZWRWYWxpZGF0aW9uU2VydmVyQ0EuY3J0MAwGA1UdEwEB/wQCMAAwggF+Bgor
BgEEAdZ5AgQCBIIBbgSCAWoBaAB3AKS5CZC0GFgUh7sTosxncAo8NZgE+RvfuON3
zQ7IDdwQAAABZTquQ3wAAAQDAEgwRgIhAMvZlCpgP2+v8gH82y3PQoMNVUVQNBjG
4DZy7qRFBo0JAiEAkzEfNkc2/B+88VR3QjutnaF1Qpj0QkSodPGAtB377UUAdQBW
FAaaL9fC7NP14b1Esj7HRna5vJkRXMDvlJhV1onQ3QAAAWU6rkPZAAAEAwBGMEQC
IHAvzbsYhbMy5jUazj6X3mDMjjyryN5BMwbDIFv58T9nAiBxzUIRTfj+Kevp0mmO
Oe9q6K/klOU2klRuVmcs7Gzw8AB2ALvZ37wfinG1k5Qjl6qSe0c4V5UKq1LoGpCW
ZDaOHtGFAAABZTquRGgAAAQDAEcwRQIhAMvzcJw5loOfVnDNFEr4+c4y/usA2pU5
M7vhHND680tHAiASqPd7KXNaNTJsBJ9IfBN6J2XwGJjxccRy9fJc9+UgYjANBgkq
hkiG9w0BAQsFAAOCAQEAoeuef8cXLigvTQs4lbtbyp4UOIzspiMmHztqB95OS0ER
/u7995SO0C0mQjvyPeiptQ5Yh+/OVCqV6p2ZpBmSc+mn5tzjP3LaVxoyjwghja03
mNBXPmdkEIG+V78Ov5iIm6vxGH1xSjHssV8iXpWo3gJ+xH3krtY1Atkg243JgwNC
I3xgp01VMLAmvIvvTqmIKeEd88Ukc6kHcZsEjxwtNivWx2nl1cyDu9B1wJK0D5Mu
IBXgbFKmqUhWlEXRimphvONOJGd71qT94bT/+bhq28oGleH1leTvqft0fj+e/a7e
Hx1u3fYAxNWjNAImIxpGUyUwSVo29w/CYYc2cS69y6GB7TCB6jCBqQIBATALBgcq
hkjOOAQDBQAwLjELMAkGA1UEBhMCdXMxDDAKBgNVBAoTA3N1bjERMA8GA1UEAxMI
aGFuZmVpeXUXDTA1MDEwNzIwMDkxMFoXDTA2MDEwNzIwMDkxMFowSTAjAgMBCTIX
DTA1MDEwNzIwMDkxMFowDTALBgNVHRUEBAoCAQQwIgICMDkXDTA1MDEwNzIwMDkx
MFowDTALBgNVHRUEBAoCAQEwCwYHKoZIzjgEAwUAAy8AMCwCFFbxw8qxTDJqc8H9
O1QIkzwkkvJfAhRF5zFU8mFsrKmnE50ERySS8vA6AKGCAh8wggIbMIIBAwIBATAN
BgkqhkiG9w0BAQsFADBsMQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQg
SW5jMRkwFwYDVQQLExB3d3cuZGlnaWNlcnQuY29tMSswKQYDVQQDEyJEaWdpQ2Vy
dCBIaWdoIEFzc3VyYW5jZSBFViBSb290IENBFw0xOTA1MDIyMjE1NTRaFw0xOTA1
MjMyMjE1NTRaMDEwLwIQDPWCOBgZnlb4K9ZS7Sft6RcNMTgxMDI1MTYxMTM4WjAM
MAoGA1UdFQQDCgEAoDAwLjAfBgNVHSMEGDAWgBSxPsNpA/i/RwHUmCYaCALvY2Qr
wzALBgNVHRQEBAICAcQwDQYJKoZIhvcNAQELBQADggEBABPO3OA0OkQZ+RLVxz/c
Nx5uNVEO416oOePkN0A4DxFztf337caS4OyfS9Wyu1j5yUdWJVpAKXSQeN95MqHk
pSpYDssuqbuYjv8ViJfseGBgtXTczUzzNeNdY2uxMbCxuhmPkgacAo1lx9LkK2Sc
YHWVbfFRF1UQ/dcmavaZsEOBNuLWOxQYA9MqfVNAymHe7vPqwm/8IY2FbHe9HsiJ
ZfGxNWMDP5lmJiXmpntTeDQ2UjdiyXwGGKjyiSTFk2jVRutrGINufaoA/f7eCmIb
4UDPbpMjVfD215dW8eBKouypCVoEvmCSSTacdiBI2yOluvMN0PzvPve0ECAE+D4e
m9Y=
"""

    def setUp(self):
        self.asn1Spec = rfc7296.CertificateBundle()

    def testDerCodec(self):
        substrate = pem.readBase64fromText(self.cert_bundle_pem_text)
        asn1Object, rest = der_decoder(substrate, asn1Spec=self.asn1Spec)

        self.assertFalse(rest)
        self.assertTrue(asn1Object.prettyPrint())
        self.assertEqual(substrate, der_encoder(asn1Object))

        cert_count = 0
        crl_count = 0
        unk_count = 0

        for item in asn1Object:
            if item.getName() == 'cert':
                cert_count += 1

            elif item.getName() == 'crl':
                crl_count += 1

            else:
                unk_count += 1

        self.assertEqual(3, cert_count)
        self.assertEqual(2, crl_count)
        self.assertEqual(0, unk_count)


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)
