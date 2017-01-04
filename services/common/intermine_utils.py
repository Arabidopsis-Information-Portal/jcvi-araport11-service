from os.path import join as urljoin
from intermine.webservice import Service

import services.common.tools as tools

# ThaleMine root API
THALEMINE_BASE_URL = 'https://apps.araport.org/thalemine/service'
service = Service(THALEMINE_BASE_URL)

TAXID = "3702"

def get_features(refseq, start, end, strand, featuretype="gene", completely_within=True, level=2):
    """
    Return the features within a given set of chromosome coordinates
    """
    url = urljoin(THALEMINE_BASE_URL, "jbrowse", TAXID, "features", refseq)
    data = tools.do_request(url, None, start=start, end=end, type=featuretype)

    elems_to_delete = []
    for x, elem0 in enumerate(data['features']):
        # remove feature if not completely_within specified chromosome coordinates
        if completely_within and ((elem0['start'] + 1) < start or elem0['end'] > end):
            elems_to_delete.append(x)
            continue
        # remove all subfeatures below 0th-level object
        if level == 0:
            data['features'][x]['subfeatures'] = []
        # remove all subfeatures below 1st-level object
        elif level == 1:
            for y, elem1 in enumerate(elem0['subfeatures']):
                data['features'][x]['subfeatures'][y]['subfeatures'] = []

            if featuretype.endswith('RNA'):
                # infer CDS parts from {exon parts + total CDS span}
                cdsPartsToAdd, cdsPartsToRemove = infer_cds_coords(elem0)

                # remove unspliced CDS parts
                cdsPartsToRemove.sort(reverse=True)
                for c in cdsPartsToRemove:
                    del data['features'][x]['subfeatures'][c]

                # add inferred CDS parts
                data['features'][x]['subfeatures'].extend(cdsPartsToAdd)

                # sort all subfeatures by start coordinates
                data['features'][x]['subfeatures'].sort(key=lambda f: f['start'], reverse=False)
        elif level == 2:
            if featuretype.endswith('Gene'):
                # infer CDS parts from {exon parts + total CDS span}
                for y, elem1 in enumerate(elem0['subfeatures']):
                    cdsPartsToAdd, cdsPartsToRemove = infer_cds_coords(elem1)

                    # remove unspliced CDS parts
                    cdsPartsToRemove.sort(reverse=True)
                    for c in cdsPartsToRemove:
                        del data['features'][x]['subfeatures'][y]['subfeatures'][c]

                    # add inferred CDS parts
                    data['features'][x]['subfeatures'][y]['subfeatures'].extend(cdsPartsToAdd)

                    # sort all subfeatures by start coordinates
                    data['features'][x]['subfeatures'][y]['subfeatures'].sort(key=lambda f: f['start'], reverse=False)

    for i in sorted(elems_to_delete, reverse=True):
        del data['features'][i]

    return data

def infer_cds_coords(feat):
    """
    Given a JBrowse JSON object representing a 2-level feature (of type RNA),
    iterate through all exon subfeatures and infer the CDS coordinates
    """
    parent = feat['uniqueID']
    strand = feat['strand']
    exons, cdsPartsToRemove, cdsPartsToAdd = [], [], []
    cdsStart, cdsEnd = float("inf"), -float("inf")

    for y, subfeat in enumerate(feat['subfeatures']):
        ftype = subfeat['type']
        fStart, fEnd = subfeat['start'], subfeat['end']
        if ftype == 'exon':
            exons.append(subfeat)
        elif ftype == 'CDS':
            # if CDS parts already exist, don't do anything
            if ':CDS:' in subfeat['uniqueID']:
                return cdsPartsToAdd, cdsPartsToRemove

            # otherwise, identify CDS span start and end to use for inference calculations
            if cdsStart > fStart: cdsStart = fStart
            if cdsEnd < fEnd: cdsEnd = fEnd
            cdsPartsToRemove.append(y)

    # bail if we don't have exons/CDS
    if not (len(exons) > 0 and cdsStart < float("inf") and cdsEnd > -float("inf")):
        return cdsPartsToAdd, []

    # sort exons by coordinates
    exons.sort(key=lambda x: x['start'], reverse=False)

    for e, exon in enumerate(exons):
        cdsPartStart, cdsPartEnd = float("inf"), -float("inf")
        exonStart, exonEnd = exon['start'], exon['end']
        if cdsStart >= exonStart and cdsStart < exonEnd:  # first exon
            cdsPartStart, cdsPartEnd = cdsStart, exonEnd
        elif cdsEnd > exonStart and cdsEnd <= exonEnd:    # last exon
            cdsPartStart, cdsPartEnd = exonStart, cdsEnd
        elif exonStart < cdsEnd and exonEnd > cdsStart:   # internal exon
            cdsPartStart, cdsPartEnd = exonStart, exonEnd

        # don't process exon if not overlapping CDS span
        if cdsPartStart == cdsPartEnd == float("inf"):
            continue

        featId = "{0}:{1}:{2}".format(parent, 'CDS', e + 1)
        # create CDS part object and store in list
        cdsPart = {
            'start': cdsPartStart,
            'end': cdsPartEnd,
            'strand': strand,
            'type': 'CDS',
            'name': featId,
            'uniqueID': featId,
            'subfeatures' : []
        }
        cdsPartsToAdd.append(cdsPart)

    return cdsPartsToAdd, cdsPartsToRemove

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
