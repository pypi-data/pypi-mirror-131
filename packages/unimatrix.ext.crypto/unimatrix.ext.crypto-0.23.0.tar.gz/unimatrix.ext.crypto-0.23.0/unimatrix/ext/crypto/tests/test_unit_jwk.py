# pylint: skip-file
import unittest

from cryptography.hazmat.primitives.asymmetric import ec

from unimatrix.ext import crypto
from ..ec import EllipticCurvePrivateKey
from ..pkcs import RSAPrivateKey


class SECP256R1TestCase(unittest.TestCase):
    key_class = EllipticCurvePrivateKey
    curve = ec.SECP256R1
    ser_jwk = {
        "crv":"P-256",
        "kty":"EC",
        "x":"7nLBMcTobLB-HULk-SOtwf8_t-kUY99ifSiM4AsWees",
        "y":"miaX9qGLT6E24Q8sgpAWnzViDyMnB7JiVqyhU5_IHX8"
    }

    def setUp(self):
        self.key = self.generate_key()
        self.pub = self.key.get_public_key()
        self.pub_jwk = self.pub.jwk

    def generate_key(self):
        return self.key_class.generate(self.curve)

    def test_fromjwk_public(self):
        k = self.pub.fromjwk(self.pub_jwk)
        self.assertEqual(self.pub.keyid, k.keyid)

    def test_fromjwk_public_nopadding(self):
        crypto.fromjwk(self.ser_jwk)


class SECP256K1TestCase(SECP256R1TestCase):
    key_class = EllipticCurvePrivateKey
    curve = ec.SECP256K1


class RSATestCase(SECP256R1TestCase):
    key_class = RSAPrivateKey
    ser_jwk = {
        "alg":"RS256",
        "e":"AQAB",
        "kty":"RSA",
        "n": (
            "qEAQ_FF1hQmt7T6_uQSNuesDMIp6JqIrj5e12SaF7HTA0kmz4NX8jjRrB9J"
            "F3CQF1LzbZfCUvy9LZc8LMGPJViQpG4rwJJiWZjTktsLFfowvDhZry0EfwR"
            "4auGoqjbkIvxNPBZxCwnt_pW7prfrbmKnXqrBqW5qgRLSnDOQq-Wvwn4R8k"
            "rjYukAkZtL446q81QQdiKOc883uOsunUa7a-UbH9npvSHbQBX0YJddvYsWY"
            "sK8jOF629o8gXiTg4HzOAXCt3oRhV6DlwljvLVkTtBrOJjhy9c7UjEX8XPJ"
            "ja_VALGKBObz8M9-6ZHjK59E_acj8pCd9nuRb0Fv08iKXoDWNQ-M0gfCgjJ"
            "wf6ItSih77rcYPvBl9AJ0kMoMWZJy7IaT6VLHNpgfIKQxGGfSZ4mlrSw1f7"
            "yyTOGAHvp-ttHne128Dpz-JzB1EFRy8GQxCqCtDMwg5xe2HfeOG3KOX8XLH"
            "nK0pq3srL7m2xLAOKeaBNFwm6R-jkca53K5hbxnHu0-M1_Y0Zb-mclvhv6p"
            "Y6HJ1Ad94HmcR37L67WyVoDjZBdA-2Z-_SviI2HKa9J04XQOHlpGY4anaVA"
            "5QfSwX9-Hr_HgUNSG8mgURyLfjPFACP9mMOMXvU5vMPegU4c8DdPYeWiXB3"
            "WJaUxDRe2Ve4C82GIUQ-LA9MIGeFFXfwgs"
        )
    }

    def generate_key(self):
        return self.key_class.generate()
