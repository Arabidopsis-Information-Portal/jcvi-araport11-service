import re
import json

import tools


def fail(message):
    # This is a simple failure message generator for generic ADAMA adapters
    # It will eventually be replaced with a system-wide fail function
    return 'text/plaintext; charset=ISO-8859-1', message


def search(args):
    chrom = args['chr']
    start = args['start']
    end = args['end']
    strand = '+' if 'strand' not in args \
            else args['strand']
    featuretype = 'gene' if 'featuretype' not in args \
            else args['featuretype']

    data = tools.parse_gff(chrom=chrom, start=start, \
        end=end, strand=strand, featuretype=featuretype)

    if data:
        return 'application/json', tools.sendJBrowse(data)
    else:
        return fail('Failed to parse gff')


def list(args):
    stats = args['stats']

    out = dict()
    if stats == 'global':
        out = { 'scoreMin': -1, 'scoreMax': 1 }

    return 'application/json', json.dumps(out)
