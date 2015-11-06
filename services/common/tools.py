import json
import os.path as op
import re
import requests
import urllib
import urlparse
from intermine.webservice import Service

# ThaleMine root API
THALEMINE_BASE_URL = 'https://apps.araport.org/thalemine/service'
service = Service(THALEMINE_BASE_URL)

gff_file = op.join(op.dirname(__file__), 'data', 'input.gff3')

def read_index(gff_file, inmemory=False):
    """
    Read in a gffutils index for fast retrieval of features.
    """
    import gffutils
    from subprocess import call

    gff_file_db = "{0}.db".format(gff_file)
    gff_file_db_gz = "{0}.gz".format(gff_file_db)

    if inmemory:
        return gffutils.create_db(gff_file, ':memory:')

    if op.exists(gff_file_db_gz):
        call('gunzip {0}'.format(gff_file_db_gz), \
            shell=True, executable='/bin/bash')

    if op.exists(gff_file_db):
        return gffutils.FeatureDB(gff_file_db)

    return gffutils.create_db(gff_file)

def parse_gff(chrom, start, end, strand, featuretype, level):
    """Parse GFF and return JSON."""

    db = read_index(gff_file)

    response_body = { 'features' : [] }
    region = "{0}:{1}-{2}".format(chrom, start, end)
    for parent in db.region(region=region, strand=strand, featuretype=featuretype):
        _strand = 1 if parent.strand == '+' else \
            (-1 if parent.strand == '-' else 0)
        pfeat = {
            'start' : parent.start,
            'end' : parent.end,
            'strand' : _strand,
            'uniqueID' : parent.id,
            'name' : parent.attributes.get('Name', [parent.id])[0],
            'description' : parent.attributes.get('Note', None)[0],
            'type' : featuretype,
            'score' : parent.score if (isinstance(parent.score, (int, float))) else 0,
        }

        cfeats = dict()
        for _level in xrange(level, 0, -1):
            for child in db.children(parent, order_by=('start'), level=_level):
                _strand = 1 if child.strand == '+' else \
                    (-1 if child.strand == '-' else 0)
                _parent = child.attributes.get('Parent')[0]
                if _parent not in cfeats: cfeats[_parent] = []
                cfeat = {
                    'start' : child.start,
                    'end' : child.end,
                    'strand' : _strand,
                    'uniqueID' : child.id,
                    'name' : child.attributes.get('Name', [child.id])[0],
                    'type' : child.featuretype,
                    'score' : child.score if (isinstance(child.score, (int, float))) else 0
                }
                if child.featuretype.endswith('codon') or child.featuretype == 'CDS':
                    cfeat['phase'] = child.frame
                if child.id in cfeats:
                    cfeat['subfeatures'] = cfeats[child.id]
                cfeats[_parent].append(cfeat)

        if parent.id in cfeats:
            pfeat['subfeatures'] = cfeats[parent.id]

        response_body['features'].append(pfeat)

    return response_body

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

def sendJBrowse(data):
    """Display `data` in the format required by JBrowse.

    """
    return json.dumps(data)

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
