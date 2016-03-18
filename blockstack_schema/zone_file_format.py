from zone_file import make_zone_file

def make_zone_file_for_hosted_data(origin, token_file_url, ttl=3600):
    if "://" not in token_file_url:
        raise ValueError("Invalid token file URL")
    json_zone_file = {
        "$ttl": ttl,
        "$origin": origin,
        "uri": [{
            "name": "@",
            "priority": 10,
            "weight": 1,
            "target": token_file_url
        }]
    }
    zone_file = make_zone_file(json_zone_file)
    return zone_file
