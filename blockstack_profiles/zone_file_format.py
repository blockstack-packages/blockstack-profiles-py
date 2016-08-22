import json
import requests
from blockstack_zones import make_zone_file, parse_zone_file

from .legacy_format import is_profile_in_legacy_format
from .token_verifying import get_profile_from_tokens


def make_zone_file_for_hosted_data(origin, token_file_url, ttl=3600):
    if "://" not in token_file_url:
        raise ValueError("Invalid token file URL")
    json_zone_file = {
        "$ttl": ttl,
        "$origin": origin,
        "uri": [{
            "name": "_http._tcp",
            "priority": 10,
            "weight": 1,
            "target": token_file_url
        }]
    }
    zone_file = make_zone_file(json_zone_file)
    return zone_file


def get_token_file_url_from_zone_file(zone_file):
    token_file_url = None

    if isinstance(zone_file, dict):
        pass
    elif isinstance(zone_file, (str, unicode)):
        zone_file = dict(parse_zone_file(zone_file))
    else:
        raise ValueError("Invalid zone file format")

    if "uri" not in zone_file:
        return token_file_url

    if isinstance(zone_file["uri"], list) and len(zone_file["uri"]) > 0:
        if "target" in zone_file["uri"][0]:
            first_uri_record = zone_file["uri"][0]
            token_file_url = first_uri_record["target"]

    return token_file_url


def zone_file_has_a_valid_uri_record(data):
    return get_token_file_url_from_zone_file(data) is not None


def resolve_zone_file_to_profile(zone_file, address_or_public_key):
    """ Resolves a zone file to a profile and checks to makes sure the tokens
        are signed with a key that corresponds to the address or public key
        provided.
    """
    if is_profile_in_legacy_format(zone_file):
        return zone_file

    try:
        token_file_url = get_token_file_url_from_zone_file(zone_file)
    except Exception as e:
        raise Exception("Token file URL could not be extracted from zone file")

    try:
        r = requests.get(token_file_url)
    except Exception as e:
        raise Exception("Token could not be acquired from token file URL")

    try:
        profile_token_records = json.loads(r.text)
    except ValueError:
        raise Exception("Token records could not be extracted from token file")

    try:
        profile = get_profile_from_tokens(profile_token_records,
                                          address_or_public_key)
    except Exception as e:
        raise Exception("Profile could not be extracted from token records")

    return profile
