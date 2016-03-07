import json
import traceback
import unittest
from test import test_support
from keychain import PrivateKeychain, PublicKeychain
from pybitcoin import BitcoinPrivateKey, BitcoinPublicKey
from blockstack_profiles import sign_profile_tokens, get_profile_from_tokens, \
    create_zone_file, get_person_from_legacy_format 

reference_profiles = {
    "legacy_1": {
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
    },
    "legacy_2": {
        "data_record": {
            "avatar": {
                "url": "https://s3.amazonaws.com/kd4/muneeb"
            },
            "bio": "Co-founder of Onename (YC S14), final-year PhD candidate at Princeton. Interested in distributed systems and blockchains.",
            "bitcoin": {
                "address": "1LNLCwtigWAvLkNakUK4jnmmvdVvmULeES"
            },
            "cover": {
                "url": "https://s3.amazonaws.com/dx3/muneeb"
            },
            "facebook": {
                "proof": {
                    "url": "https://facebook.com/muneeb.ali/posts/10152524743274123"
                },
                "username": "muneeb.ali"
            },
            "github": {
                "proof": {
                    "url": "https://gist.github.com/muneeb-ali/9838362"
                },
                "username": "muneeb-ali"
            },
            "graph": {
                "followee_count": 4,
                "url": "https://s3.amazonaws.com/grph/muneeb"
            },
            "location": {
                "formatted": "New York, NY"
            },
            "name": {
                "formatted": "Muneeb Ali"
            },
            "pgp": {
                "fingerprint": "9862A3FB338BE9EB6C6A5E05639C89272AFEC540",
                "url": "http://muneebali.com/static/files/key.asc"
            },
            "twitter": {
                "proof": {
                    "url": "https://twitter.com/muneeb/status/483765788478689280"
                },
                "username": "muneeb"
            },
            "v": "0.2",
            "website": "http://muneebali.com"
        }
    }
}

class TokeningTests(unittest.TestCase):
    def setUp(self):
        self.master_private_key = BitcoinPrivateKey(compressed=True)

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
        # print json.dumps(profile_token_records, indent=2)
        self.assertTrue(isinstance(profile_token_records, list))
        # recover the profile
        profile = get_profile_from_tokens(
            profile_token_records, self.master_private_key.public_key().to_hex())
        # print json.dumps(profile, indent=2)
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
        # print json.dumps(zone_file, indent=2)
        self.assertTrue(isinstance(zone_file, dict))

class LegacyFormatTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_profile_format_migration(self):
        zone_file = get_person_from_legacy_format(reference_profiles["legacy_1"])
        # print json.dumps(zone_file, indent=2, sort_keys=True)
        self.assertTrue(isinstance(zone_file, dict))

    def test_profile_format_migration_2(self):
        zone_file = get_person_from_legacy_format(reference_profiles["legacy_2"])
        # print json.dumps(zone_file, indent=2, sort_keys=True)
        self.assertTrue(isinstance(zone_file, dict))


def test_main():
    test_support.run_unittest(
        TokeningTests,
        ZonefileTests,
        LegacyFormatTests
    )


if __name__ == '__main__':
    test_main()
