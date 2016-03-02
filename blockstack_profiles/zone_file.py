
def create_zone_file(origin, token_file_url):
    if "://" not in token_file_url:
        raise ValueError("Invalid token file URL")

    url_parts = token_file_url.split("://")[1].split("/")
    domain = url_parts[0]
    pathname = "/" + "/".join(url_parts[1:])

    zone_file = {
        "$origin": origin,
        "$ttl": 3600,
        "cname": [
            { "name": "@", "alias": domain }
        ],
        "txt": [
            { "name": "@", "txt": "pathname: " + pathname }
        ]
    }

    return zone_file
