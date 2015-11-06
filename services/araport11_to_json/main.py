import json
import services.common.tools as tools

def search(args):
    """
    args contains a dict with one or key:values

    locus is AGI identifier and is mandatory
    """
    search_locus = args['locus']
    token = args['_token']

    # get the chromosome coordinates of the specified locus
    coordinates = tools.get_gene_coordinates(search_locus)
    if not coordinates:
        raise Exception("Locus '%s' could not be found!" % search_locus)

    # get all of the overlapping features in jBrowse format from the araport11_gff_to_jbrowse service
    url = 'https://api.araport.org/community/v0.3/araport/araport11_gff_to_jbrowse_v0.1/search'
    payload = {
        'q': 'features',
        'chr': coordinates['chromosome'],
        'start': coordinates['start'],
        'end': coordinates['end'],
        'strand': coordinates['strand'],
        'featuretype': 'gene',
        'level': 2
    }
    data = tools.do_request(url, token, **payload)
    return 'application/json', json.dumps(data)

def list(args):
    """
    List all of the valid AGI gene locus identifiers from Araport11
    """
    # get a new query on the class (table) from the model
    query = tools.service.new_query("Gene")

    # views specify the output columns
    query.add_view("primaryIdentifier", "chromosomeLocation.end", "chromosomeLocation.start")

    ids = []
    for row in query.rows():
        record = {
            'locus': row['primaryIdentifier']
        }
        ids.append(record)
    return 'application/json', json.dumps(ids)
