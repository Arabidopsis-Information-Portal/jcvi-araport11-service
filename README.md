# Araport11 Webservices

These are [Araport](http://www.araport.org) services that can parse Araport11 GFF3 files, extract information (including features), and convert them into a JSON format.

## araport11_to_json
Given a valid AGI locus return it's features from the Araport11 Pre-Release 2 (10/2015) annotation in JSON format consumable by the jBrowse genome browser. This service uses ThaleMine to retrieve chromosome location information and the **araport11_gff_to_jbrowse** service to extract the features.
```
$ http "https://api.araport.org/community/v0.3/araport/araport11_to_json_v1.1/search?locus=AT1G65480" Authorization:"Bearer $TOKEN"
{
    "features": [
        {
            "description": "PEBP (phosphatidylethanolamine-binding protein) family protein",
            "end": 24333999,
            "name": "AT1G65480",
            "score": 0,
            "start": 24331373,
            "strand": 1,
            "subfeatures": [
                {
                    "end": 24333999,
                    "name": "AT1G65480.2",
                    "score": 0,
                    "start": 24331373,
                    "strand": 1,
                    "subfeatures": [
                        {
                            "end": 24331710,
                            "name": "FT:exon:1",
                            "score": 0,
                            "start": 24331373,
                            "strand": 1,
                            "type": "exon",
                            "uniqueID": "AT1G65480:exon:1"
                        },
                        {
                            "end": 24331377,
                            "name": "FT:five_prime_UTR:1",
                            "score": 0,
                            "start": 24331373,
                            "strand": 1,
                            "type": "five_prime_UTR",
                            "uniqueID": "AT1G65480:five_prime_UTR:1"
                        },
                        {
                            "end": 24331710,
                            "name": "FT:CDS:1",
                            "phase": "0",
                            "score": 0,
                            "start": 24331378,
                            "strand": 1,
                            "type": "CDS",
                            "uniqueID": "AT1G65480:CDS:1"
                        },
                        {
                            "end": 24332587,
                            "name": "FT:CDS:3",
                            "phase": "0",
                            "score": 0,
                            "start": 24332526,
                            "strand": 1,
                            "type": "CDS",
                            "uniqueID": "AT1G65480:CDS:3"
                        },
                        {
                            "end": 24332587,
                            "name": "FT:exon:3",
                            "score": 0,
                            "start": 24332526,
                            "strand": 1,
                            "type": "exon",
                            "uniqueID": "AT1G65480:exon:3"
                        },
                        {
                            "end": 24333341,
                            "name": "FT:CDS:4",
                            "phase": "1",
                            "score": 0,
                            "start": 24333301,
                            "strand": 1,
                            "type": "CDS",
                            "uniqueID": "AT1G65480:CDS:4"
                        },
                        {
                            "end": 24333341,
                            "name": "FT:exon:4",
                            "score": 0,
                            "start": 24333301,
                            "strand": 1,
                            "type": "exon",
                            "uniqueID": "AT1G65480:exon:4"
                        },
                        {
                            "end": 24333689,
                            "name": "FT:CDS:5",
                            "phase": "2",
                            "score": 0,
                            "start": 24333466,
                            "strand": 1,
                            "type": "CDS",
                            "uniqueID": "AT1G65480:CDS:5"
                        },
                        {
                            "end": 24333999,
                            "name": "FT:exon:6",
                            "score": 0,
                            "start": 24333466,
                            "strand": 1,
                            "type": "exon",
                            "uniqueID": "AT1G65480:exon:6"
                        },
                        {
                            "end": 24333999,
                            "name": "FT:three_prime_UTR:2",
                            "score": 0,
                            "start": 24333690,
                            "strand": 1,
                            "type": "three_prime_UTR",
                            "uniqueID": "AT1G65480:three_prime_UTR:2"
                        }
                    ],
                    "type": "mRNA",
                    "uniqueID": "AT1G65480.2"
                },
                {
                    "end": 24333935,
                    "name": "AT1G65480.1",
                    "score": 0,
                    "start": 24331428,
                    "strand": 1,
                    "subfeatures": [
                        {
                            "end": 24331710,
                            "name": "FT:exon:2",
                            "score": 0,
                            "start": 24331428,
                            "strand": 1,
                            "type": "exon",
                            "uniqueID": "AT1G65480:exon:2"
                        },
                        {
                            "end": 24331509,
                            "name": "FT:five_prime_UTR:2",
                            "score": 0,
                            "start": 24331428,
                            "strand": 1,
                            "type": "five_prime_UTR",
                            "uniqueID": "AT1G65480:five_prime_UTR:2"
                        },
                        {
                            "end": 24331710,
                            "name": "FT:CDS:2",
                            "phase": "0",
                            "score": 0,
                            "start": 24331510,
                            "strand": 1,
                            "type": "CDS",
                            "uniqueID": "AT1G65480:CDS:2"
                        },
                        {
                            "end": 24332587,
                            "name": "FT:CDS:3",
                            "phase": "0",
                            "score": 0,
                            "start": 24332526,
                            "strand": 1,
                            "type": "CDS",
                            "uniqueID": "AT1G65480:CDS:3.1"
                        },
                        {
                            "end": 24333341,
                            "name": "FT:CDS:4",
                            "phase": "1",
                            "score": 0,
                            "start": 24333301,
                            "strand": 1,
                            "type": "CDS",
                            "uniqueID": "AT1G65480:CDS:4.1"
                        },
                        {
                            "end": 24333689,
                            "name": "FT:CDS:5",
                            "phase": "2",
                            "score": 0,
                            "start": 24333466,
                            "strand": 1,
                            "type": "CDS",
                            "uniqueID": "AT1G65480:CDS:5.1"
                        },
                        {
                            "end": 24333935,
                            "name": "FT:exon:5",
                            "score": 0,
                            "start": 24333466,
                            "strand": 1,
                            "type": "exon",
                            "uniqueID": "AT1G65480:exon:5"
                        },
                        {
                            "end": 24333935,
                            "name": "FT:three_prime_UTR:1",
                            "score": 0,
                            "start": 24333690,
                            "strand": 1,
                            "type": "three_prime_UTR",
                            "uniqueID": "AT1G65480:three_prime_UTR:1"
                        }
                    ],
                    "type": "mRNA",
                    "uniqueID": "AT1G65480.1"
                }
            ],
            "type": "gene",
            "uniqueID": "AT1G65480"
        }
    ]
}
```

## araport11_gff_to_jbrowse
Given a desired range parse the Araport11 GFF, extract features, and return data in JBrowse compatible JSON format.
```
$ http "https://api.araport.org/community/v0.3/araport/araport11_gff_to_jbrowse_v0.1/search?q=features&chr=Chr1&start=216843&end=225822&featuretype=mRNA" Authorization:"Bearer $TOKEN"
{
    "features": [
        {
            "description": "ferric reduction oxidase 1",
            "end": 217734,
            "name": "AT1G01590.1",
            "score": 0,
            "start": 214150,
            "strand": 1,
            "subfeatures": [
                {
                    "end": 214406,
                    "name": "FRO1:exon:1",
                    "score": 0,
                    "start": 214150,
                    "strand": 1,
                    "type": "exon",
                    "uniqueID": "AT1G01590:exon:1"
                },
                {
                    "end": 214228,
                    "name": "FRO1:five_prime_UTR:1",
                    "score": 0,
                    "start": 214150,
                    "strand": 1,
                    "type": "five_prime_UTR",
                    "uniqueID": "AT1G01590:five_prime_UTR:1"
                },
                {
                    "end": 214406,
                    "name": "FRO1:CDS:1",
                    "phase": "0",
                    "score": 0,
                    "start": 214229,
                    "strand": 1,
                    "type": "CDS",
                    "uniqueID": "AT1G01590:CDS:1"
                },
                {
                    "end": 214582,
                    "name": "FRO1:CDS:2",
                    "phase": "2",
                    "score": 0,
                    "start": 214480,
                    "strand": 1,
                    "type": "CDS",
                    "uniqueID": "AT1G01590:CDS:2"
                },
                {
                    "end": 214582,
                    "name": "FRO1:exon:2",
                    "score": 0,
                    "start": 214480,
                    "strand": 1,
                    "type": "exon",
                    "uniqueID": "AT1G01590:exon:2"
                },
                {
                    "end": 214897,
                    "name": "FRO1:CDS:3",
                    "phase": "1",
                    "score": 0,
                    "start": 214697,
                    "strand": 1,
                    "type": "CDS",
                    "uniqueID": "AT1G01590:CDS:3"
                },
                {
                    "end": 214897,
                    "name": "FRO1:exon:3",
                    "score": 0,
                    "start": 214697,
                    "strand": 1,
                    "type": "exon",
                    "uniqueID": "AT1G01590:exon:3"
                },
                {
                    "end": 215554,
                    "name": "FRO1:CDS:4",
                    "phase": "1",
                    "score": 0,
                    "start": 215317,
                    "strand": 1,
                    "type": "CDS",
                    "uniqueID": "AT1G01590:CDS:4"
                },
                {
                    "end": 215554,
                    "name": "FRO1:exon:4",
                    "score": 0,
                    "start": 215317,
                    "strand": 1,
                    "type": "exon",
                    "uniqueID": "AT1G01590:exon:4"
                },
                {
                    "end": 215960,
                    "name": "FRO1:CDS:5",
                    "phase": "0",
                    "score": 0,
                    "start": 215633,
                    "strand": 1,
                    "type": "CDS",
                    "uniqueID": "AT1G01590:CDS:5"
                },
                {
                    "end": 215960,
                    "name": "FRO1:exon:5",
                    "score": 0,
                    "start": 215633,
                    "strand": 1,
                    "type": "exon",
                    "uniqueID": "AT1G01590:exon:5"
                },
                {
                    "end": 216293,
                    "name": "FRO1:CDS:6",
                    "phase": "2",
                    "score": 0,
                    "start": 216044,
                    "strand": 1,
                    "type": "CDS",
                    "uniqueID": "AT1G01590:CDS:6"
                },
                {
                    "end": 216293,
                    "name": "FRO1:exon:6",
                    "score": 0,
                    "start": 216044,
                    "strand": 1,
                    "type": "exon",
                    "uniqueID": "AT1G01590:exon:6"
                },
                {
                    "end": 217090,
                    "name": "FRO1:CDS:7",
                    "phase": "1",
                    "score": 0,
                    "start": 216414,
                    "strand": 1,
                    "type": "CDS",
                    "uniqueID": "AT1G01590:CDS:7"
                },
                {
                    "end": 217090,
                    "name": "FRO1:exon:7",
                    "score": 0,
                    "start": 216414,
                    "strand": 1,
                    "type": "exon",
                    "uniqueID": "AT1G01590:exon:7"
                },
                {
                    "end": 217304,
                    "name": "FRO1:CDS:8",
                    "phase": "2",
                    "score": 0,
                    "start": 217165,
                    "strand": 1,
                    "type": "CDS",
                    "uniqueID": "AT1G01590:CDS:8"
                },
                {
                    "end": 217734,
                    "name": "FRO1:exon:8",
                    "score": 0,
                    "start": 217165,
                    "strand": 1,
                    "type": "exon",
                    "uniqueID": "AT1G01590:exon:8"
                },
                {
                    "end": 217734,
                    "name": "FRO1:three_prime_UTR:1",
                    "score": 0,
                    "start": 217305,
                    "strand": 1,
                    "type": "three_prime_UTR",
                    "uniqueID": "AT1G01590:three_prime_UTR:1"
                }
            ],
            "type": "mRNA",
            "uniqueID": "AT1G01590.1"
        },
        {
            "description": "cytochrome P450%2C family 86%2C subfamily A%2C polypeptide 4",
            "end": 221286,
            "name": "AT1G01600.1",
            "score": 0,
            "start": 218834,
            "strand": 1,
            "subfeatures": [
                {
                    "end": 219621,
                    "name": "CYP86A4:exon:1",
                    "score": 0,
                    "start": 218834,
                    "strand": 1,
                    "type": "exon",
                    "uniqueID": "AT1G01600:exon:1"
                },
                {
                    "end": 219199,
                    "name": "CYP86A4:five_prime_UTR:1",
                    "score": 0,
                    "start": 218834,
                    "strand": 1,
                    "type": "five_prime_UTR",
                    "uniqueID": "AT1G01600:five_prime_UTR:1"
                },
                {
                    "end": 219621,
                    "name": "CYP86A4:CDS:1",
                    "phase": "0",
                    "score": 0,
                    "start": 219200,
                    "strand": 1,
                    "type": "CDS",
                    "uniqueID": "AT1G01600:CDS:1"
                },
                {
                    "end": 220994,
                    "name": "CYP86A4:CDS:2",
                    "phase": "1",
                    "score": 0,
                    "start": 219752,
                    "strand": 1,
                    "type": "CDS",
                    "uniqueID": "AT1G01600:CDS:2"
                },
                {
                    "end": 221286,
                    "name": "CYP86A4:exon:2",
                    "score": 0,
                    "start": 219752,
                    "strand": 1,
                    "type": "exon",
                    "uniqueID": "AT1G01600:exon:2"
                },
                {
                    "end": 221286,
                    "name": "CYP86A4:three_prime_UTR:1",
                    "score": 0,
                    "start": 220995,
                    "strand": 1,
                    "type": "three_prime_UTR",
                    "uniqueID": "AT1G01600:three_prime_UTR:1"
                }
            ],
            "type": "mRNA",
            "uniqueID": "AT1G01600.1"
        },
        {
            "description": "glycerol-3-phosphate acyltransferase 4",
            "end": 224351,
            "name": "AT1G01610.1",
            "score": 0,
            "start": 221642,
            "strand": -1,
            "subfeatures": [
                {
                    "end": 222359,
                    "name": "GPAT4:exon:4",
                    "score": 0,
                    "start": 221642,
                    "strand": -1,
                    "type": "exon",
                    "uniqueID": "AT1G01610:exon:4"
                },
                {
                    "end": 221949,
                    "name": "GPAT4:three_prime_UTR:1",
                    "score": 0,
                    "start": 221642,
                    "strand": -1,
                    "type": "three_prime_UTR",
                    "uniqueID": "AT1G01610:three_prime_UTR:1"
                },
                {
                    "end": 222359,
                    "name": "GPAT4:CDS:4",
                    "phase": "2",
                    "score": 0,
                    "start": 221950,
                    "strand": -1,
                    "type": "CDS",
                    "uniqueID": "AT1G01610:CDS:4"
                },
                {
                    "end": 223096,
                    "name": "GPAT4:CDS:3",
                    "phase": "0",
                    "score": 0,
                    "start": 222622,
                    "strand": -1,
                    "type": "CDS",
                    "uniqueID": "AT1G01610:CDS:3"
                },
                {
                    "end": 223096,
                    "name": "GPAT4:exon:3",
                    "score": 0,
                    "start": 222622,
                    "strand": -1,
                    "type": "exon",
                    "uniqueID": "AT1G01610:exon:3"
                },
                {
                    "end": 223866,
                    "name": "GPAT4:CDS:2",
                    "phase": "1",
                    "score": 0,
                    "start": 223551,
                    "strand": -1,
                    "type": "CDS",
                    "uniqueID": "AT1G01610:CDS:2"
                },
                {
                    "end": 223866,
                    "name": "GPAT4:exon:2",
                    "score": 0,
                    "start": 223551,
                    "strand": -1,
                    "type": "exon",
                    "uniqueID": "AT1G01610:exon:2"
                },
                {
                    "end": 224255,
                    "name": "GPAT4:CDS:1",
                    "phase": "0",
                    "score": 0,
                    "start": 223945,
                    "strand": -1,
                    "type": "CDS",
                    "uniqueID": "AT1G01610:CDS:1"
                },
                {
                    "end": 224351,
                    "name": "GPAT4:exon:1",
                    "score": 0,
                    "start": 223945,
                    "strand": -1,
                    "type": "exon",
                    "uniqueID": "AT1G01610:exon:1"
                },
                {
                    "end": 224351,
                    "name": "GPAT4:five_prime_UTR:1",
                    "score": 0,
                    "start": 224256,
                    "strand": -1,
                    "type": "five_prime_UTR",
                    "uniqueID": "AT1G01610:five_prime_UTR:1"
                }
            ],
            "type": "mRNA",
            "uniqueID": "AT1G01610.1"
        },
        {
            "description": "plasma membrane intrinsic protein 1C",
            "end": 227302,
            "name": "AT1G01620.2",
            "score": 0,
            "start": 225665,
            "strand": -1,
            "subfeatures": [
                {
                    "end": 226081,
                    "name": "PIP1C:exon:6",
                    "score": 0,
                    "start": 225665,
                    "strand": -1,
                    "type": "exon",
                    "uniqueID": "AT1G01620:exon:6"
                },
                {
                    "end": 225985,
                    "name": "PIP1C:three_prime_UTR:1",
                    "score": 0,
                    "start": 225665,
                    "strand": -1,
                    "type": "three_prime_UTR",
                    "uniqueID": "AT1G01620:three_prime_UTR:1"
                },
                {
                    "end": 226081,
                    "name": "PIP1C:CDS:5",
                    "phase": "0",
                    "score": 0,
                    "start": 225986,
                    "strand": -1,
                    "type": "CDS",
                    "uniqueID": "AT1G01620:CDS:5"
                },
                {
                    "end": 226311,
                    "name": "PIP1C:CDS:4",
                    "phase": "0",
                    "score": 0,
                    "start": 226171,
                    "strand": -1,
                    "type": "CDS",
                    "uniqueID": "AT1G01620:CDS:4"
                },
                {
                    "end": 226311,
                    "name": "PIP1C:exon:5",
                    "score": 0,
                    "start": 226171,
                    "strand": -1,
                    "type": "exon",
                    "uniqueID": "AT1G01620:exon:5"
                },
                {
                    "end": 226691,
                    "name": "PIP1C:CDS:3",
                    "phase": "2",
                    "score": 0,
                    "start": 226396,
                    "strand": -1,
                    "type": "CDS",
                    "uniqueID": "AT1G01620:CDS:3"
                },
                {
                    "end": 226691,
                    "name": "PIP1C:exon:4",
                    "score": 0,
                    "start": 226396,
                    "strand": -1,
                    "type": "exon",
                    "uniqueID": "AT1G01620:exon:4"
                },
                {
                    "end": 226960,
                    "name": "PIP1C:CDS:2",
                    "phase": "0",
                    "score": 0,
                    "start": 226849,
                    "strand": -1,
                    "type": "CDS",
                    "uniqueID": "AT1G01620:CDS:2"
                },
                {
                    "end": 227049,
                    "name": "PIP1C:exon:3",
                    "score": 0,
                    "start": 226849,
                    "strand": -1,
                    "type": "exon",
                    "uniqueID": "AT1G01620:exon:3"
                },
                {
                    "end": 227049,
                    "name": "PIP1C:five_prime_UTR:3",
                    "score": 0,
                    "start": 226961,
                    "strand": -1,
                    "type": "five_prime_UTR",
                    "uniqueID": "AT1G01620:five_prime_UTR:3"
                },
                {
                    "end": 227302,
                    "name": "PIP1C:exon:1",
                    "score": 0,
                    "start": 227079,
                    "strand": -1,
                    "type": "exon",
                    "uniqueID": "AT1G01620:exon:1"
                },
                {
                    "end": 227302,
                    "name": "PIP1C:five_prime_UTR:2",
                    "score": 0,
                    "start": 227079,
                    "strand": -1,
                    "type": "five_prime_UTR",
                    "uniqueID": "AT1G01620:five_prime_UTR:2"
                }
            ],
            "type": "mRNA",
            "uniqueID": "AT1G01620.2"
        },
        {
            "description": "plasma membrane intrinsic protein 1C",
            "end": 227543,
            "name": "AT1G01620.1",
            "score": 0,
            "start": 225665,
            "strand": -1,
            "subfeatures": [
                {
                    "end": 226081,
                    "name": "PIP1C:CDS:5",
                    "phase": "0",
                    "score": 0,
                    "start": 225986,
                    "strand": -1,
                    "type": "CDS",
                    "uniqueID": "AT1G01620:CDS:5.1"
                },
                {
                    "end": 226311,
                    "name": "PIP1C:CDS:4",
                    "phase": "0",
                    "score": 0,
                    "start": 226171,
                    "strand": -1,
                    "type": "CDS",
                    "uniqueID": "AT1G01620:CDS:4.1"
                },
                {
                    "end": 226691,
                    "name": "PIP1C:CDS:3",
                    "phase": "2",
                    "score": 0,
                    "start": 226396,
                    "strand": -1,
                    "type": "CDS",
                    "uniqueID": "AT1G01620:CDS:3.1"
                },
                {
                    "end": 227176,
                    "name": "PIP1C:CDS:1",
                    "phase": "0",
                    "score": 0,
                    "start": 226849,
                    "strand": -1,
                    "type": "CDS",
                    "uniqueID": "AT1G01620:CDS:1"
                },
                {
                    "end": 227543,
                    "name": "PIP1C:exon:2",
                    "score": 0,
                    "start": 226849,
                    "strand": -1,
                    "type": "exon",
                    "uniqueID": "AT1G01620:exon:2"
                },
                {
                    "end": 227543,
                    "name": "PIP1C:five_prime_UTR:1",
                    "score": 0,
                    "start": 227177,
                    "strand": -1,
                    "type": "five_prime_UTR",
                    "uniqueID": "AT1G01620:five_prime_UTR:1"
                }
            ],
            "type": "mRNA",
            "uniqueID": "AT1G01620.1"
        }
    ]
}
```
