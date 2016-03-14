from zone_file import make_zone_file

def make_zone_file_for_hosted_file(origin, token_file_url, ttl=3600):
    if "://" not in token_file_url:
        raise ValueError("Invalid token file URL")
    records = [{
        "name": "@", 
        "class": "IN",
        "type": "URI",
        "data": token_file_url
    }]
    zone_file = make_zone_file(origin, ttl, records)
    return zone_file
