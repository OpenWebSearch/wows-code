import os
import pyterrier as pt

pt.init(packages=["com.github.terrierteam:terrier-ciff:-SNAPSHOT"])

for representation in ["title", "description", "content"]:
    index_path = f"./index-{representation}/data.properties"
    if not os.path.exists(index_path):
        pt.run('ciff-ingest', ['-I', index_path, f"index-{representation}.ciff"])
