import glob
#import gzip
import rdflib
import sys
import os
import re

infolder = sys.argv[1]
outfolder = sys.argv[2]
prefix = sys.argv[3]
lang = sys.argv[4]
if(lang==None):
    lang = "de"

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

#for gz in glob.glob(infolder+"/"+prefix+"*.ttl.gz"):
for gz in glob.glob(infolder+"/"+prefix+"*.ttl"):
    for ig in ignore:
        if(ig in gz):
            continue
    print(gz)
    #outname = gz.replace("000001.ttl.gz",".nt").replace(prefix,"").replace(infolder,outfolder+"/"+prefix)
    outname = gz.replace("000001","").replace(".ttl",".nt").replace(prefix,"").replace(infolder,outfolder+"/"+prefix)
    #stream = gzip.open(gz,"rt")
    stream = open(gz,"rt")
    turtle = stream.read()
    turtle = fixuris(turtle)
    g = rdflib.Graph()
    g.parse(publicID="/" ,format="n3",data=turtle)
    unsorted = g.serialize(format="nt", encoding=None)
    lines = sorted(unsorted.splitlines())
    nt = b"\n".join(lines).decode("utf-8")
    print(outname)
    outdir = outfolder+"/"+prefix
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    file = open(outname,"w")
    file.write(nt)
