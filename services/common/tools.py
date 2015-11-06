import json
import re
import requests
import urllib
import urlparse
from intermine.webservice import Service

# ThaleMine root API
THALEMINE_BASE_URL = 'https://apps.araport.org/thalemine/service'
service = Service(THALEMINE_BASE_URL)

def get_gene_coordinates(locus):
    """
    Return the chromosome coordinates of a gene given a locus identifier
    """
    query = service.new_query("Gene")

    query.add_constraint("chromosomeLocation.feature.primaryIdentifier", "=", locus, code = "A")

    query.add_view("chromosomeLocation.start","chromosomeLocation.end", "chromosome.primaryIdentifier", "chromosomeLocation.strand")

    for row in query.rows():
        strand = ''
        if row["chromosomeLocation.strand"]:
            if int(row["chromosomeLocation.strand"]) > 0:
                strand = '+'
            else:
                strand = '-'
        coordinates = {
            'chromosome': row["chromosome.primaryIdentifier"],
            'start': row["chromosomeLocation.start"],
            'end': row["chromosomeLocation.end"],
            'strand': strand
        }
    return coordinates

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

def send(data):
    """Display `data` in the format required by Adama.
    :type data: list
    """

    for elt in data:
        print json.dumps(elt)
        print '---'

def fail(message):
    # failure message for generic adapters
    return 'text/plaintext; charset=ISO-8859-1', message
