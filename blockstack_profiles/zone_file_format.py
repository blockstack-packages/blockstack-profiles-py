import json
import requests
from blockstack_zones import make_zone_file, parse_zone_file

from .legacy_format import is_profile_in_legacy_format
from .token_verifying import get_profile_from_tokens


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

