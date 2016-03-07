import json
import traceback
import unittest
from test import test_support
from keychain import PrivateKeychain, PublicKeychain
from pybitcoin import BitcoinPrivateKey, BitcoinPublicKey
from blockstack_profiles import sign_profile_tokens, get_profile_from_tokens, \
    create_zone_file, get_person_from_legacy_format 


class TokeningTests(unittest.TestCase):
    def setUp(self):
        self.master_private_key = BitcoinPrivateKey()

    def tearDown(self):
        pass

    def test_basic_tokening(self):
        profile_components = [
            {"name": "Naval Ravikant"},
            {"birthDate": "1980-01-01"}
        ]
        reference_profile = {
            "name": "Naval Ravikant", 
            "birthDate": "1980-01-01"
        }
        # tokenize the profile
        profile_token_records = sign_profile_tokens(
            profile_components, self.master_private_key.to_hex())
        print json.dumps(profile_token_records, indent=2)
        self.assertTrue(isinstance(profile_token_records, list))
        # recover the profile
        profile = get_profile_from_tokens(
            profile_token_records, self.master_private_key.public_key().to_hex())
        print json.dumps(profile, indent=2)
        self.assertTrue(isinstance(profile, object))
        self.assertEqual(profile, reference_profile)


class ZonefileTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_zone_file_creation(self):
        origin = "naval.id"
        token_file_url = "https://mq9.s3.amazonaws.com/naval.id/profile.json"
        zone_file = create_zone_file(origin, token_file_url)
        print json.dumps(zone_file, indent=2)
        self.assertTrue(isinstance(zone_file, dict))

    def test_profile_format_migration(self):
        legacy_profile = {
            "data_record": {
                "avatar": {
                    "url": "https://s3.amazonaws.com/kd4/judecn"
                },
                "bio": "PhD student",
                "bitcoin": {
                    "address": "17zf596xPvV8Z8ThbWHZHYQZEURSwebsKE"
                },
                "cover": {
                    "url": "https://s3.amazonaws.com/97p/gQZ.jpg"
                },
                "facebook": {
                    "proof": {
                        "url": "https://facebook.com/sunspider/posts/674912239245011"
                    },
                    "username": "sunspider"
                },
                "github": {
                    "proof": {
                        "url": "https://gist.github.com/jcnelson/70c02f80f8d4b0b8fc15"
                    },
                    "username": "jcnelson"
                },
                "location": {
                    "formatted": "Princeton University"
                },
                "name": {
                    "formatted": "Jude Nelson"
                },
                "twitter": {
                    "proof": {
                        "url": "https://twitter.com/judecnelson/status/507374756291555328"
                    },
                    "username": "judecnelson"
                },
                "v": "0.2",
                "website": "http://www.cs.princeton.edu/~jcnelson"
            }
        }
        zone_file = get_person_from_legacy_format( legacy_profile )
        print json.dumps(zone_file, indent=2, sort_keys=True)
        self.assertTrue(isinstance(zone_file, dict))

def test_main():
    test_support.run_unittest(
        TokeningTests,
        ZonefileTests
    )


if __name__ == '__main__':
    test_main()
