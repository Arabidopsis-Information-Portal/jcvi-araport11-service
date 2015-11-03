import json
import os.path as op

gff_file = op.join(op.dirname(__file__), 'data', 'input.gff3')

def read_index(gff_file, inmemory=False):
    """
    Read in a gffutils index for fast retrieval of features.
    """
    import gffutils
    from subprocess import call

    gff_file_db = "{0}.db".format(gff_file)
    gff_file_db_gz = "{0}.gz".format(gff_file_db)

    if inmemory:
        return gffutils.create_db(gff_file, ':memory:')

    if op.exists(gff_file_db_gz):
        call('gunzip {0}'.format(gff_file_db_gz), \
            shell=True, executable='/bin/bash')

    if op.exists(gff_file_db):
        return gffutils.FeatureDB(gff_file_db)

    return gffutils.create_db(gff_file)


def parse_gff(chrom, start, end, strand, featuretype):
    """Parse GFF and return JSON."""

    db = read_index(gff_file)

    response_body = { 'features' : [] }
    region = "{0}:{1}-{2}".format(chrom, start, end)
    for parent in db.region(region=region, strand=strand, featuretype=featuretype):
        _strand = 1 if parent.strand == '+' else \
            (-1 if parent.strand == '-' else 0)
        pfeat = {
            'start' : parent.start,
            'end' : parent.end,
            'strand' : _strand,
            'uniqueID' : parent.id,
            'name' : parent.attributes.get('Name', [parent.id])[0],
            'description' : parent.attributes.get('Note', None)[0],
            'type' : featuretype,
            'score' : parent.score if (isinstance(parent.score, (int, float))) else 0,
            'subfeatures': []
        }
        for child in db.children(parent):
            _strand = 1 if child.strand == '+' else \
                (-1 if child.strand == '-' else 0)
            cfeat = {
                'start' : child.start,
                'end' : child.end,
                'strand' : _strand,
                'uniqueID' : child.id,
                'name' : child.attributes.get('Name', [child.id])[0],
                'type' : child.featuretype,
                'score' : child.score if (isinstance(child.score, (int, float))) else 0
            }
            if child.featuretype.endswith('codon') or child.featuretype == 'CDS':
                cfeat['phase'] = child.frame
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
