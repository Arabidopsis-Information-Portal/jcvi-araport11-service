import json
import re
import requests


def to_camel_case(snake_str):
    """Convert input snake_str to CamelCase"""
    components = snake_str.split('_')
    camel_str = "".join(x.title() for x in components)

    # specifically address RNA/CDS feature types
    for s in ["RNA", "CDS"]:
        regex = re.compile(s.lower(), re.IGNORECASE)
        camel_str = regex.sub(s, camel_str)

    return camel_str

def do_request(url, token, **kwargs):
    """Perform a request to SITE and return JSON."""

    headers = {}
    if token:
        headers["Authorization"] = "Bearer %s" % token
    response = requests.get(url, headers=headers, params=kwargs)

    # Raise exception and abort if requests is not successful
    response.raise_for_status()

    try:
        # Try to convert result to JSON
        # abort if not possible
        return response.json()
    except ValueError:
        raise Exception('not a JSON object: {}'.format(response.text))

def do_request_generic(url, token, **kwargs):
    """Perform a request to SITE and return response."""

    headers = {}
    if token:
        headers["Authorization"] = "Bearer %s" % token
    response = requests.get(url, headers=headers, params=kwargs)

    # Raise exception and abort if requests is not successful
    response.raise_for_status()

    return response

def is_valid_agi_identifier(ident):
    p = re.compile(r'AT[1-5MC]G[0-9]{5,5}\.[0-9]+', re.IGNORECASE)
    if not p.search(ident):
        return False
    return True

def sendList(data):
    """Display `data` in the format required by Adama.
    :type data: list
    """

    for elt in data:
        print json.dumps(elt)
        print '---'

def send(data):
    """Display `data` in the format required by Adama.

    """
    print json.dumps(data)
    print '---'

def fail(message):
    # failure message for generic adapters
    return 'text/plaintext; charset=ISO-8859-1', message
