import glob
import gzip
import rdflib
import sys
import os
import re

if(len(sys.argv)<4):
    print("Usage: virtuoso2git infolder outfolder prefix [lang]")
    sys.exit(1)

infolder = sys.argv[1]
outfolder = sys.argv[2]
prefix = sys.argv[3]
lang = sys.argv[4]
if(lang==None):
    lang = "de"
suffix = "000001"

# some releases around 0.8 had some literals with spaces mistakenly modelled as URIs, which breaks N-Triples serialization.
def fixuris(s):
    uris = re.findall(r"<[^>]*\\u00[^>]*>", s)
    for broken in uris:
        if(broken.startswith("<http://")):
            continue
        fixed = '"'+re.sub(r'[^-,.;\wäüöÖÜÄß ]',"",broken.encode('raw-unicode-escape').decode("unicode-escape"))+'"'
        s = s.replace(broken,fixed+"@"+lang)        
    #s = s.encode("raw-unicode-escape").decode("unicode-escape")
    return s

ignore = ["meta"]

ttl = infolder+"/"+prefix+"*.ttl"
files = [f for f in [glob.glob(p) for p in [ttl,ttl+".gz"]] for f in f]

if(len(files)<1):
    print("No files found in folder",infolder)
    sys.exit(1)

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
    turtle = fixuris(turtle)
    g = rdflib.Graph()
    try:
        g.parse(publicID="/" ,format="n3",data=turtle)
        unsorted = g.serialize(format="nt", encoding=None)
        lines = sorted(unsorted.splitlines())
        nt = b"\n".join(lines).decode("utf-8")
        outdir = outfolder+"/"+prefix
        if not os.path.exists(outdir):
            os.mkdir(outdir)
        file = open(outpath,"w")
        print("Write",outpath)
        file.write(nt)
    except rdflib.plugins.parsers.notation3.BadSyntax: 
        print("Cannot parse file ",f)
        continue
