import json
import os.path as op
import services.common.tools as tools
import services.common.intermine_utils as utils

def search(args):
    """
    args contains a dict with one or key:values

    locus is AGI identifier and is mandatory
    """
    search_locus = args['locus']
    _url, token = args['_url'], args['_token']

    # get the chromosome coordinates of the specified locus
    coordinates = utils.get_gene_coordinates(search_locus)
    if not coordinates:
        raise Exception("Locus '%s' could not be found!" % search_locus)

    # get all of the overlapping features in jBrowse format from the araport11_gff_to_jbrowse service
    url = op.join(_url, 'araport', 'araport11_gff_region_to_jbrowse_v0.1', 'search')
    payload = {
        'q': 'features',
        'chr': coordinates['chromosome'],
        'start': coordinates['start'],
        'end': coordinates['end'],
        'strand': coordinates['strand'],
        'featuretype': 'gene',
        'level': 2,
        'completely_within': True
        'interbase' : False
    }
    data = tools.do_request(url, token, **payload)
    return 'application/json', json.dumps(data)

def list(args):
    """
    List all of the valid AGI gene locus identifiers from Araport11
    """
    ids = utils.get_gene_identifiers()

    return 'application/json', json.dumps(ids)
