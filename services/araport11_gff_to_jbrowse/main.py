import json
import services.common.tools as tools

def search(args):
    q = args['q']
    chrom = args['chr']
    start = args['start']
    end = args['end']
    if start >= end:
        tools.fail('End coordinate must be greater than start')
    strand = None if 'strand' not in args \
            else args['strand']
    featuretype = args['featuretype']
    level = args['level']

    if q == 'features':
        data = tools.parse_gff(chrom=chrom, start=start, \
            end=end, strand=strand, featuretype=featuretype, level=level)

        if not data:
            return tools.fail('Failed to parse gff')
    elif q == 'globalStats':
        data = { 'scoreMin': -1, 'scoreMax': 1 }

    return 'application/json', tools.sendJBrowse(data)


def list(args):
    import requests

    url = 'https://api.araport.org/community/v0.3/aip/get_sequence_by_coordinate_v0.3/list'
    token = args['_token']

    response = requests.get(url, \
        headers={ 'Authorization': 'Bearer {0}'.format(token) })

    # Raise exception and abort if requests is not successful
    response.raise_for_status()

    data = None
    try:
        # Try to convert result to JSON
        # abort if not possible
        data = response.json()
    except ValueError:
        raise Exception('not a JSON object: {}'.format(response.text))

    return 'application/json', data
