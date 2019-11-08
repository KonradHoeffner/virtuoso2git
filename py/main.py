import glob
import gzip
import rdflib
import sys
import os

ignore = ["meta"]

infolder = sys.argv[1]
outfolder = sys.argv[2]
prefix = sys.argv[3] 
for gz in glob.glob(infolder+"/"+prefix+"*.ttl.gz"):
    for ig in ignore:
        if(ig in gz):
            continue
    outname = gz.replace("000001.ttl.gz",".nt").replace(prefix,"").replace(infolder,outfolder+"/"+prefix)
    stream = gzip.open(gz,"rt")
    turtle = stream.read()
    g = rdflib.Graph()
    g.parse(None,None,"n3",None,None,turtle)
    unsorted = g.serialize(format="nt", encoding=None)
    lines = sorted(unsorted.splitlines())
    nt = b"\n".join(lines).decode("utf-8")
    print(outname)
    outdir = outfolder+"/"+prefix
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    file = open(outname,"w")
    file.write(nt)
