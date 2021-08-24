# virtuoso2git

Create git commits out of Virtuoso SPARQL RDF Dumps.

## Usage

    virtuoso2git infolder outfolder prefix

## Requirements

* install Python 3
* `pip install rdflib`

## SNIK Example

1. Create stored procedures `dump_one_graph` and `dump_graphs` from <http://vos.openlinksw.com/owiki/wiki/VOS/VirtRDFDatasetDump#Dump%20One%20Graph> (just once)
2. Use `dump_one_graph` on all the graphs in <https://www.snik.eu/conductor> -> Database -> Interactive SQL, where YYYYMMDD is the date, for example 20210519 with meta: `dump_one_graph ('http://www.snik.eu/ontology/meta', './dumps/YYYYMMDDmeta', 1000000000);`
3. Download the dumps from the bruchtal server via `scp -r root@bruchtal:/var/lib/docker/volumes/sniktoolset_virtuoso-data/_data/dumps .`
4. virtuoso2git /myfolder/dumps . 20210519
