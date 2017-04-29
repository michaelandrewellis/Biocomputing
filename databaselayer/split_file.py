import re

# ---------------------------------------------------------------------------

#This code splits the chromosome 15 file into 241 files - one for each locus.

with open('chrom_CDS_15','r') as f:
    data = f.read()
found = re.findall(r'\n*(LOCUS.*?\n\/\/)\n*', data, re.M|re.S)
#looks between the start of the file (at LOCUS) and the end of the file (at //)
[open(str(i)+'.txt', 'w').write(found[i-1]) for i in range(1, len(found)+1)]
#writes the detected chunks into individual files


# ---------------------------------------------------------------------------