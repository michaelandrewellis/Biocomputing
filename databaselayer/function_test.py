import re
import os
indir = '/Users/ainefairbrother/PycharmProjects/BiocomputingII/genes'

with open('chrom_CDS_15') as f:
    original_file = f.read().splitlines()

file_name_compiler = re.compile(r'(\d+)')
def numerical_sort(value):                              #DO DOCSTRING FOR THIS
    separator = file_name_compiler.split(value)
    separator[1::2] = map(int, separator[1::2])
    return separator

# ---------------------------------------------------------------------------------------------------

gene_ids = []                                                               ## gene IDs
id_compiler = re.compile(r"^LOCUS\s+(\w+).+\/\/", re.MULTILINE|re.DOTALL)
"""
for root, dirs, all_files in os.walk(indir):
    for infile in sorted(all_files, key=numerical_sort):
        open_file = open(os.path.join(root, infile), 'r')
        match_id = id_compiler.search(open_file.read())
        if match_id:
            gene_ids.append(str(match_id.group(1)))
        else:
           gene_ids.append(str('none'))
"""

def file_iterator(list, compiler, else_statement = None):
    for root, dirs, all_files in os.walk(indir):
        for infile in sorted(all_files, key=numerical_sort):
            open_file = open(os.path.join(root, infile), 'r')
            match = compiler.search(open_file.read())
            if match:
                list.append(str(match.group(1)))
            else:
                list.append(str(else_statement))
    return()

file_iterator(gene_ids, id_compiler)

print(len(gene_ids))