import json
import requests
import os.path as op

import services.common.tools as tools
import services.common.intermine_utils as utils

def search(args):
    """
    Return features within a chromosomal region in JBrowse JSON format
    """
    q = args['q']
    chrom = None if 'chr' not in args \
            else args['chr']
    start = None if 'start' not in args \
            else args['start']
    end = None if 'end' not in args \
            else args['end']
    if start >= end:
        tools.fail('End coordinate must be greater than start')
    strand = None if 'strand' not in args \
            else args['strand']
    featuretype = 'gene' if 'featuretype' not in args \
            else args['featuretype']
    completely_within = False if 'completely_within' not in args \
            else args['completely_within']
    if 'level' not in args:
        level = 0
        if featuretype.endswith('gene'):
            level = 2
        elif featuretype.endswith('RNA') or featuretype.endswith('transcript') or \
            featuretype.endswith('match') or featuretype.endswith('region'):
            level = 1
    else:
        level = args['level']
    interbase = True if 'interbase' not in args \
            else args['interbase']

    imfeatureclass = tools.to_camel_case(featuretype)
    if q == 'features':
        data = utils.get_features(refseq=chrom, start=start, \
            end=end, strand=strand, featuretype=imfeatureclass, \
            level=level, completely_within=completely_within, \
            interbase=interbase)

        if not data:
            return tools.fail('Failed to retrieve feature data in JSON')
    elif q == 'globalStats':
        data = utils.get_global_stats(featuretype=imfeatureclass)
    elif q == 'regionStats':
        data = utils.get_region_stats(refseq=chrom, start=start, \
            end=end, featuretype=imfeatureclass)
    elif q == 'regionFeatureDensities':
        data = utils.get_region_feature_densities(refseq=chrom, start=start, \
            end=end, featuretype=imfeatureclass)

    return 'application/json', json.dumps(data)


def list(args):
    """
    List all of the valid Arabidopsis chromosomes and their lengths
    """
    _url, token = args['_url'], args['_token']
    url = op.join(_url, 'aip', 'get_sequence_by_coordinate_v0.3', 'list')

    data = tools.do_request(url, token)

    return 'application/json', json.dumps(data)
