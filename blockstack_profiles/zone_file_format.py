from zone_file import make_zone_file

def make_zone_file_for_hosted_data(origin, token_file_url, ttl=3600):
    if "://" not in token_file_url:
        raise ValueError("Invalid token file URL")
    records = {
        "URI": [
            {
                "name": "@",
                "weight": 1,
                "priority": 10,
                "target": token_file_url
            }
        ]
    }
    zone_file = make_zone_file(records, origin=origin, ttl=ttl)
    return zone_file
