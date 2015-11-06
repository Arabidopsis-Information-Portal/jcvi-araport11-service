from intermine.webservice import Service

# ThaleMine root API
THALEMINE_BASE_URL = 'https://apps.araport.org/thalemine/service'
service = Service(THALEMINE_BASE_URL)


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
