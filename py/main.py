import glob
import gzip
import rdflib
import sys
import os
import re

if(len(sys.argv)<3):
    print("Usage: virtuoso2git infolder outfolder prefix")
    sys.exit(1)

infolder = sys.argv[1]
outfolder = sys.argv[2]
prefix = sys.argv[3]
suffix = "000001"

ignore = ["meta"]

ttl = infolder+"/"+prefix+"*.ttl"
files = [f for f in [glob.glob(p) for p in [ttl,ttl+".gz"]] for f in f]

if(len(files)<1):
    print("No files found in folder",infolder)
    sys.exit(1)

if not os.path.exists(outfolder):
    os.mkdir(outfolder)

for f in files:
    for ig in ignore:
        if(ig in f):
            continue
    print("Read",f)
    outname = re.search(prefix+r"(.*)"+suffix,f).group(1) + ".nt"
    outpath = outfolder + "/" + outname
    
    if(f.endswith(".gz")):
        stream = gzip.open(f,"rt")
    else:
        stream = open(f,"rt")
    turtle = stream.read()
    g = rdflib.Graph()
    try:
        g.parse(publicID="/" ,format="n3",data=turtle)
        print("Write",outpath)
        g.serialize(destination=outpath,format="nt", encoding=None)
        os.system("LC_ALL=en_US.UTF-8 sort "+outpath+" -o "+outpath) # fix locale to prevent diffs across different locales
    except rdflib.plugins.parsers.notation3.BadSyntax: 
        print("Cannot parse file ",f)
        continue
