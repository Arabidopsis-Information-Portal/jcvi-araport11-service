import json
import requests
import os.path as op

import services.common.tools as tools
import services.common.gff_utils as utils

gff_file = op.join(op.dirname(__file__), 'data', 'input.gff3')

def search(args):
    """
    Return features within a chromosomal region in JBrowse JSON format
    """
    q = args['q']
    chrom = args['chr']
    start = args['start']
    end = args['end']
    if start >= end:
        tools.fail('End coordinate must be greater than start')
    strand = None if 'strand' not in args \
            else args['strand']
    featuretype = 'mRNA' if 'featuretype' not in args \
            else args['featuretype']
    level = 1 if 'level' not in args \
            else args['level']
    completely_within = False if 'completely_within' not in args \
            else args['completely_within']
    interbase = True if 'interbase' not in args \
            else args['interbase']

    if q == 'features':
        data = utils.parse_gff(gff_file, chrom=chrom, start=start, \
            end=end, strand=strand, featuretype=featuretype, level=level, \
            completely_within=completely_within)

        if not data:
            return tools.fail('Failed to parse gff')
    elif q == 'globalStats':
        data = { 'scoreMin': -1, 'scoreMax': 1 }
    elif q == 'regionStats':
        raise Exception('Not implemented yet')
    elif q == 'regionFeatureDensities':
        raise Exception('Not implemented yet')

    return 'application/json', json.dumps(data)


def list(args):
    """
    List all of the valid Arabidopsis chromosomes and their lengths
    """
    _url, token = args['_url'], args['_token']
    url = op.join(_url, 'aip', 'get_sequence_by_coordinate_v0.3', 'list')

    data = tools.do_request(url, token)

    return 'application/json', json.dumps(data)
