from os.path import join as urljoin
from intermine.webservice import Service

import services.common.tools as tools

# ThaleMine root API
THALEMINE_BASE_URL = 'https://apps.araport.org/thalemine/service'
service = Service(THALEMINE_BASE_URL)

TAXID = "3702"

def get_features(refseq, start, end, strand, featuretype="gene", level=2, completely_within=False, interbase=True):
    """
    Return the features within a given set of chromosome coordinates
    """
    url = urljoin(THALEMINE_BASE_URL, "jbrowse", TAXID, "features", refseq)
    data = tools.do_request(url, None, start=start, end=end, type=featuretype)

    # Remove any features not on specified strand
    if strand:
        featsToRemove = remove_features_not_on_strand(data, strand=strand)
        for i in sorted(featsToRemove, reverse=True):
            del data['features'][i]

    # By default, data from ThaleMine is returned in 0-based (interbase) format
    if not interbase:
        data = convert_to_1based(data)

    elemsToDelete = []
    for x, elem0 in enumerate(data['features']):
        if completely_within and (elem0['start'] < start or elem0['end'] > end):
            # remove feature if not completely_within specified chromosome coordinates
            elemsToDelete.append(x)
            continue
        if level == 0:
            # remove all subfeatures below 0th-level object
            data['features'][x]['subfeatures'] = []
        elif level == 1:
            # remove all subfeatures below 1st-level object
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

    for i in sorted(elemsToDelete, reverse=True):
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

    # bail if we don't have exons and CDS
    if not (len(exons) > 0 and len(cdsPartsToRemove) > 0):
        return cdsPartsToAdd, []

    # sort exons by coordinates
    exons.sort(key=lambda x: x['start'], reverse=False)

    for e, exon in enumerate(exons):
        cdsPartStart, cdsPartEnd = float("inf"), -float("inf")
        exonStart, exonEnd = exon['start'], exon['end']
        if (cdsStart > exonStart and cdsStart < exonEnd) and \
            (cdsEnd > exonStart and cdsEnd < exonEnd):    # CDS containing exon
            cdsPartStart, cdsPartEnd = cdsStart, cdsEnd
        elif cdsStart >= exonStart and cdsStart < exonEnd:  # 5' terminal CDS part
            cdsPartStart, cdsPartEnd = cdsStart, exonEnd
        elif cdsEnd > exonStart and cdsEnd <= exonEnd:    # 3' terminal CDS part
            cdsPartStart, cdsPartEnd = exonStart, cdsEnd
        elif exonStart < cdsEnd and exonEnd > cdsStart:   # internal CDS part
            cdsPartStart, cdsPartEnd = exonStart, exonEnd

        # don't process exon if not overlapping CDS span
        if cdsPartStart == float("inf") or cdsPartEnd == -float("inf"):
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

def remove_features_not_on_strand(data, strand):
    """
    Given a strand ("+" or "-"), iterate through all top-level features (parent)
    and discard if not on the specified strand.
    """
    featsToRemove = []
    imstrand = 1 if strand == '+' else -1
    for x, elem0 in enumerate(data['features']):
        if imstrand != int(elem0['strand']):
            featsToRemove.append(x)

    return featsToRemove

def convert_to_1based(data):
    """
    Given a JBrowse JSON feature object from ThaleMine, iterate through all
    levels and convert start coordinate from 0-based (interbase) to 1-based
    """
    for x, elem0 in enumerate(data['features']):
        data['features'][x]['start'] += 1
        for y, elem1 in enumerate(elem0['subfeatures']):
            data['features'][x]['subfeatures'][y]['start'] += 1
            for z in xrange(len(elem1['subfeatures'])):
                data['features'][x]['subfeatures'][y]['subfeatures'][z]['start'] += 1

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
