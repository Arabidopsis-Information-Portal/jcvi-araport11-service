from os.path import join as urljoin
from intermine.webservice import Service

import services.common.tools as tools

# ThaleMine root API
THALEMINE_BASE_URL = 'https://apps.araport.org/thalemine/service'
service = Service(THALEMINE_BASE_URL)

TAXID = "3702"

def get_features(refseq, start, end, strand, featuretype, completely_within=True, level=1):
    """
    Return the features within a given set of chromosome coordinates
    """
    url = urljoin(THALEMINE_BASE_URL, "jbrowse", TAXID, "features", refseq)
    data = tools.do_request(url, None, start=start, end=end, type=featuretype)

    elems_to_delete = []
    for x, elem0 in enumerate(data['features']):
        # remove feature if not completely_within specified chromosome coordinates
        if completely_within and (elem0['start'] < start or elem0['end'] > end):
            elems_to_delete.append(x)
            continue
        # remove all subfeatures below 0th-level object
        if level == 0:
            data['features'][x]['subfeatures'] = []
        # remove all subfeatures below 1st-level object
        elif level == 1:
            for y, elem1 in enumerate(elem0['subfeatures']):
                data['features'][x]['subfeatures'][y]['subfeatures'] = []

    for i in sorted(elems_to_delete, reverse=True):
        del data['features'][i]

    return data

def get_global_stats(featuretype):
    """
    Return global stats for features of specific type
    """
    url = urljoin(THALEMINE_BASE_URL, "jbrowse", TAXID, "stats", "global")
    global_stats = tools.do_request(url, None, type=featuretype)

    return global_stats

def get_region_stats(refseq, start, end, featuretype):
    """
    Return stats for features within a given set of chromosome coordinates
    """
    url = urljoin(THALEMINE_BASE_URL, "jbrowse", TAXID, "stats", "region", refseq)
    region_stats = tools.do_request(url, None, start=start, end=end, type=featuretype)

    return region_stats

def get_region_feature_densities(refseq, start, end, featuretype):
    """
    Return binned density stats for features within a given set of chromosome coordinates
    """
    url = urljoin(THALEMINE_BASE_URL, "jbrowse", TAXID, "stats", "regionFeatureDensities", refseq)
    region_feature_densities = tools.do_request(url, None, start=start, end=end, type=featuretype)

    return region_feature_densities

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

def get_gene_identifiers():
    """
    Return the list of gene identifiers from ThaleMine
    """
    # get a new query on the class (table) from the model
    query = service.new_query("Gene")

    # views specify the output columns
    query.add_view("primaryIdentifier", "chromosomeLocation.end", "chromosomeLocation.start")

    ids = []
    for row in query.rows():
        record = {
            'locus': row['primaryIdentifier']
        }
        ids.append(record)

    return ids
