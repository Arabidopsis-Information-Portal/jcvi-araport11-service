import json
import os.path as op


gff_file = op.join(op.dirname(__file__), 'data', 'TAIR10_GFF3_genes.gff')

def make_index(gff_file):
    """
    Make an inmemory index for fast retrieval of features.
    """
    import gffutils
    db_file = gff_file + ".db"

    if not op.exists(db_file):
        gffutils.create_db(gff_file, db_file)

    return gffutils.FeatureDB(db_file)


def parse_gff(chrom, start, end, strand, featuretype):
    """Parse GFF and return JSON."""

    db = make_index(gff_file)

    response_body = { 'features' : [] }
    region = "{0}:{1}-{2}".format(chrom, start, end)
    _strand = 1 if strand == "+" else 0
    for parent in db.region(region=region, strand=strand, featuretype=featuretype):
        pfeat = {
            'start' : parent.start,
            'end' : parent.end,
            'strand' : parent.strand,
            'uniqueID' : parent.id,
            'name' : parent.id,
            'type' : featuretype,
            'score' : parent.score,
            'subfeatures': []
        }
        for i, child in enumerate(db.children(parent)):
            cfeat = {
                'start' : child.start,
                'end' : child.end,
                'strand' : child.strand,
                'uniqueID' : child.id,
                'name' : child.id,
                'type' : child.featuretype,
                'score' : child.score
            }
            pfeat['subfeatures'].append(cfeat)

        response_body['features'].append(pfeat)

    return response_body


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
