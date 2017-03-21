import re

# ---------------------------------------------------------------------------

#This code splits the chromosome 15 file into individual genes

with open('chrom_CDS_15','r') as f:
    data = f.read()

found = re.findall(r'\n*(LOCUS.*?\n\/\/)\n*', data, re.M|re.S)

[open(str(i)+'.txt', 'w').write(found[i-1]) for i in range(1, len(found)+1)]

