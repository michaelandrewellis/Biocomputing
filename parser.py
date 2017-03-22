import re
import os
import pandas as pd
indir = '/Users/ainefairbrother/PycharmProjects/BiocomputingII/genes'

with open('chrom_CDS_15') as f:
    original_file = f.read().splitlines()

# ------------------------------------------------------------------------------------------------
# -----------------------------------Data extraction tier-----------------------------------------

# function to split the filenames so the directory iterator loop goes through the files in order from 1 to 241
# thus allowing all lists generated to in the same order (from gene 1 to 241)
    
file_name_compiler = re.compile(r'(\d+)')
def numerical_sort(value):                              #DO DOCSTRING FOR THIS
    separator = file_name_compiler.split(value)
    separator[1::2] = map(int, separator[1::2])
    return separator

# the following code loops through all 241 files in the directory 'genes'
# it then opens each one and searches between 'LOCUS' and '//' using the regexes
# then appends matched groups to the relevant list
# this is the method used for extracting all of the required data from the file

genbank_accessions = list()                                                 ## genbank accessions
accession_compiler = re.compile(r"^ACCESSION\s+(\w+).+\/\/", re.MULTILINE|re.DOTALL)
for root, dirs, all_files in os.walk(indir):
    for infile in sorted(all_files, key=numerical_sort):
        open_file = open(os.path.join(root, infile), 'r')
        match_acc = accession_compiler.search(open_file.read())
        if match_acc:
            genbank_accessions.append(str(match_acc.group(1)))
        else:
            genbank_accessions.append(str('none'))

gene_ids = list()                                                           ## gene IDs
id_compiler = re.compile(r"^LOCUS\s+(\w+).+\/\/", re.MULTILINE|re.DOTALL)
for root, dirs, all_files in os.walk(indir):
    for infile in sorted(all_files, key=numerical_sort):
        open_file = open(os.path.join(root, infile), 'r')
        match_id = id_compiler.search(open_file.read())
        if match_id:
            gene_ids.append(str(match_id.group(1)))
        else:
           gene_ids.append(str('none'))

dna_seq = list()                                                            
dnaseq_compiler = re.compile(r"^ORIGIN\s+(.+)\/\/", re.DOTALL|re.MULTILINE)
for root, dirs, all_files in os.walk(indir):
    for infile in sorted(all_files, key=numerical_sort):
        open_file = open(os.path.join(root, infile), 'r')
        match_seq = dnaseq_compiler.search(open_file.read())
        if match_seq:
            dna_seq.append(str(match_seq.group(1)))
        else:
            dna_seq.append(str('none'))

clean_dna_seq = list()                                                      ## DNA sequence
for x in dna_seq:
    sub1 = re.sub(r"\W", "", x)
    sub2 = re.sub(r"\d", "", sub1)
    clean_dna_seq.append(sub2)

gene_products = list()                                                      ## 1st protein product
prod_compiler = re.compile(r"^LOCUS\s.+\/product\=\"(.+?)\".+\/\/", re.MULTILINE|re.DOTALL)
for root, dirs, all_files in os.walk(indir):
    for infile in sorted(all_files, key=numerical_sort):
        open_file = open(os.path.join(root, infile), 'r')
        match_pp = prod_compiler.search(open_file.read())
        if match_pp:
            gene_products.append(str(match_pp.group(1)))
        else:
            gene_products.append(str('none'))
            
chr_loc = list()                                                            ## chromosomal location
chromosome_no = '15'
chrloc_compiler = re.compile(r"^LOCUS\s.+\/map\=\"(.+?)\".+^\/\/", re.MULTILINE|re.DOTALL)
for root, dirs, all_files in os.walk(indir):
    for infile in sorted(all_files, key=numerical_sort):
        open_file = open(os.path.join(root, infile), 'r')
        match_chrloc = chrloc_compiler.search(open_file.read())
        if match_chrloc:
            chr_loc.append(str(match_chrloc.group(1)))
        else:
            chr_loc.append(chromosome_no)

protein_seq = []
proseq_compiler = re.compile(r"^LOCUS\s.+\/translation\=\"(.+?)\".+\/\/", re.MULTILINE | re.DOTALL)
for root, dirs, all_files in os.walk(indir):
    for infile in sorted(all_files, key=numerical_sort):
        open_file = open(os.path.join(root, infile), 'r')
        match_protseq = proseq_compiler.search(open_file.read())
        if match_protseq:
            protein_seq.append(str(match_protseq.group(1)))
        else:
            protein_seq.append(str('none'))

clean_protein_seq = []                                                      ## protein sequence
for x in protein_seq:
    sub = re.sub(r"\W", "", x)
    clean_protein_seq.append(sub)

            
# --- finding the coding seq of the gene in order to extract exon boundaries --- #

ex_int_boundaries = list()
cds_compiler = re.compile(r"^LOCUS\s.+\s{5}CDS\s+(.+?)\s{1}.+\/\/", re.MULTILINE|re.DOTALL)
for root, dirs, all_files in os.walk(indir):
    for infile in sorted(all_files, key=numerical_sort):
        open_file = open(os.path.join(root, infile), 'r')
        match_cds = cds_compiler.search(open_file.read())
        if match_cds:
            ex_int_boundaries.append(match_cds.group(1))
        else:
            ex_int_boundaries.append('none')

# the following code strips off superfluous characters from items in  ex_int_boundaries:
clean_boundaries = list()
for x in ex_int_boundaries:
    sub = re.sub(r"join\(", "", x)
    sub1 = re.sub(r"\<", "", sub)
    sub2 = re.sub(r"\>", "", sub1)
    sub3 = re.sub(r"\(", "", sub2)
    sub4 = re.sub(r"\)", "", sub3)
    sub5 = re.sub(r"complement", "", sub4)
    clean_boundaries.append(sub5)

# the following code generates a list containing lists. Each sub list contains all the exon boundaries for one gene.
# some lists just have one, whereas others have multiple exons, and so have lists containing multiple terms:
exons_into_lists = list()
for x in clean_boundaries:
    no_comma = x.rstrip(',') #cuts off extra comma at the end of items in clean_boundaries
    split_to_list = list((no_comma.split(',')))
    exons_into_lists.append(split_to_list)

# the following code searches for any gene where its exons span multiple genes and replaces its exon location information
# with 'exons span multiple genes':
exon_across_genes_compiler = re.compile(r"[A-Z]{1,2}.+?\:")
remove_spans = []
phrase = 'exons span multiple genes'
for list in exons_into_lists:
    for items in list:
        match = exon_across_genes_compiler.search(items)
        if match:
            list.append(phrase)
    if phrase in list:
        l = len(list)
        chop = l - 1
        new_list = list[chop:]
        remove_spans.append(new_list)
    else:
        remove_spans.append(list)

# --- separating the start and end positions of the exons into an exon start list and an exon end list --- #

# the following code grabs all the exon start positions for a particular and puts them into a sub-list
# the sub-list is then appended to the main list:
exon_start = []                                                            # exon start positions
exon_end = []                                                              # exon end positions
exon_start_compiler = re.compile(r"^(\d+)\.")
exon_end_compiler = re.compile(r"^\d+\.\.(\d+)")
for list in remove_spans:
    start_matches = []
    if phrase in list:
        exon_start.append(phrase)
    else:
        for items in list:
            match = exon_start_compiler.search(items)
            if match:
                start_matches.append(str(match.group(1)))
        exon_start.append(start_matches)

# the following code grabs all the exon end positions for a particular and puts them into a sub-list
# the sub-list is then appended to the main list:
for list in remove_spans:
    end_matches = []
    if phrase in list:
        exon_end.append(phrase)
    else:
        for items in list:
            match = exon_end_compiler.search(items)
            if match:
                end_matches.append(str(match.group(1)))
        exon_end.append(end_matches)

# the sql import doesn't like lists of lists, so converting sub-lists into strings
str_ex_start = []
str_ex_end = []
for list in exon_start:
    str_ex_start.append(str(list))
for list in exon_end:
    str_ex_end.append(str(list))


# ------------------------------------------------------------------------------------------------
# -----------------------------------Database connection tier-------------------------------------

# Using Pandas to generate dataframes from my lists

#gene_ids                          will be 'Gene_ID' in DB
#chr_loc                           will be 'Chromosome_location' in DB
#clean_dna_seq                     will be 'DNA_sequence' in DB
#clean_protein_seq                 will be 'Protein_sequence' in DB
#gene_products                     will be 'Protein_product' in DB
#exon_start                        will be 'Start_location' in DB
#exon_end                          will be 'End_location' in DB

gene_info_df = pd.DataFrame({'Gene_ID': gene_ids, 'Chromosome_location':chr_loc, 'DNA_sequence':clean_dna_seq, 'Protein_sequence':clean_protein_seq, 'Protein_product':gene_products}, index=gene_ids)
coding_region_df = pd.DataFrame({'Gene_ID': gene_ids, 'End_location':str_ex_end, 'Start_location':str_ex_start}, index=gene_ids)

# filtering out splice variants:
pattern = "[A-Z]+\d+S"
filter = gene_info_df['Gene_ID'].str.contains(pattern)
gene_info_df = gene_info_df[~filter]
coding_region_df = coding_region_df[~filter]

import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://root:Poppeta1995@localhost:3306/biocomp_project', echo=False)
gene_info_df.to_sql(name='Gene_info', con=engine, if_exists = 'append', index=False)
coding_region_df.to_sql(name='Coding_region', con=engine, if_exists = 'append', index=False)

# ------------------------------------------------------------------------------------------------

