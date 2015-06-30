Web service wrapper to transform standalone GFF3 files into JBrowse compatible JSON
=======

Objective: Build a simple web service which can parse standalone GFF3 files, extract features of specific type,
and convert them into JSON format consumable by the JBrowse genome browser. This adapter uses [gffutils](http://pythonhosted.org/gffutils/contents.html)
to process input GFF3 files, making an intermediary sqlite database for fast data retrieval
