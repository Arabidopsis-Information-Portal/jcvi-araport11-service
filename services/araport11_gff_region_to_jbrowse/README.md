Web service wrapper to transform standalone GFF3 files into JBrowse compatible JSON
=======

Objective: Build a simple web service which can parse standalone GFF3 files, extract features of specific type, and convert them into JSON format consumable by the JBrowse genome browser. This adapter uses [gffutils](http://pythonhosted.org/gffutils/contents.html) to process input GFF3 files, making an intermediary sqlite database for fast data retrieval.

* Enable the following plugin in JBrowse within `tracks.conf`:
  * [Araport REST](https://github.com/Arabidopsis-Information-Portal/jbrowse/blob/stable/plugins/Araport/js/Store/SeqFeature/REST) with bindings to ADAMA
```
[plugins]
Araport.location = ./plugins/Araport
```

* This adapter relies on storing the GFF3 file (and gzipped intermediary sqlite database) within the repository in the `data/` sub-directory. In this example implementation, we have configured this code repository to host and serve the latest [Araport11 Release (Jun 2016)](https://www.araport.org/data/araport11) genome annotation dataset. In order to create the sqlite database and commit it into the git repository, follow the steps outlined below:
  ```
  % cd data/
  % ls *.gff
  Araport11_GFF3_genes_transposons.201606.gff
  % cp -s Araport11_GFF3_genes_transposons.201606.gff input.gff

  % python
  >>> import gffutils
  >>> gffutils.create_db('input.gff', 'input.gff.db')
  >>> Ctrl + D

  % gzip -9 input.gff.db
  % git add input.gff.db.gz
  % git commit -am 'Add custom GFF3 file'
  % git push
  ```

* Once the above step is complete, ensure that the [araport11_gff_region_to_jbrowse](https://github.com/Arabidopsis-Information-Portal/jcvi-araport11-services/tree/master/services/araport11_gff_region_to_jbrowse) adapter is registered and accessible via ADAMA. See [metadata.yml](https://github.com/Arabidopsis-Information-Portal/jcvi-araport11-services/blob/master/services/araport11_gff_region_to_jbrowse/metadata.yml) for adapter configuration (list of dependency modules and REST endpoints described using swagger.io spec).

* Set up the following track configuration in JBrowse within `trackList.json`:
```
{
   "style" : {
      "className" : "transcript",
      "subfeatureClasses" : {
         "three_prime_UTR" : "transcript-UTR",
         "exon" : "transcript-exon",
         "five_prime_UTR" : "transcript-UTR",
         "CDS" : "transcript-CDS"
      },
      "label" : "id,name"
   },
   "key" : "Araport11 Protein Coding Genes",
   "noExport" : true,
   "storeClass" : "Araport/Store/SeqFeature/REST",
   "baseUrl" : "https://api.araport.org/community/v0.3/araport/araport11_gff_region_to_jbrowse_v0.1",
   "compress" : 0,
   "type" : "FeatureTrack",
   "category" : "Araport Data / Araport11 / Annotation (Jun 2016)",
   "metadata" : {
        "Description" : "Protein coding gene models annotated as part of the Araport11 Release (Jun 2016)",
        "Source" : "Araport11 Release (Jun 2016)",
        "URL" : "https://www.araport.org/data/araport11"
    },
   "label" : "Araport11_gene_models",
   "query" : {
     "featuretype" : "mRNA"
   }
}
```

### Contributors
[Vivek Krishnakumar](https://github.com/vivekkrish) - JCVI
