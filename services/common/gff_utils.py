import json
import os.path as op
import gffutils
from subprocess import call

def read_index(gff_file, inmemory=False):
    """
    Read in a gffutils index for fast retrieval of features.
    """

    gff_file_db = "{0}.db".format(gff_file)
    gff_file_db_gz = "{0}.gz".format(gff_file_db)

    if inmemory:
        return gffutils.create_db(gff_file, ':memory:')

    if op.exists(gff_file_db_gz):
        call('gunzip {0}'.format(gff_file_db_gz), \
            shell=True, executable='/bin/bash')

    if not op.exists(gff_file_db):
        gffutils.create_db(gff_file, gff_file_db)

    return gffutils.FeatureDB(gff_file_db)


def parse_gff(gff_file, chrom, start, end, strand, featuretype, level, completely_within):
    """Parse GFF and return JSON."""

    db = read_index(gff_file)

    response_body = { 'features' : [] }
    region = "{0}:{1}-{2}".format(chrom, start, end)
    for parent in db.region(region=region, strand=strand, featuretype=featuretype, \
        completely_within=completely_within):
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
        }

        cfeats = dict()
        for _level in xrange(level, 0, -1):
            for child in db.children(parent, order_by=('start'), level=_level):
                _strand = 1 if child.strand == '+' else \
                    (-1 if child.strand == '-' else 0)
                _parent = child.attributes.get('Parent')[0]
                if _parent not in cfeats: cfeats[_parent] = []
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
                if child.id in cfeats:
                    cfeat['subfeatures'] = cfeats[child.id]
                cfeats[_parent].append(cfeat)

        if parent.id in cfeats:
            pfeat['subfeatures'] = cfeats[parent.id]

        response_body['features'].append(pfeat)

    return response_body
