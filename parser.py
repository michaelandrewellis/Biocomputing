#! /usr/bin/env python3

import re
import os
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import admin
pw = admin.password
indir = '/Users/ainefairbrother/PycharmProjects/BiocomputingII/genes'

# --------------------------------------------------------------------------------------------------
# -----------------------------------Data extraction tier-------------------------------------------

# function to split the filenames so the directory iterator loop goes through the files in order from 1 to 241
# thus allowing all lists to be generated in the same order (from gene 1 to 241)
    
file_name_compiler = re.compile(r'(\d+)')
def numerical_convert(value):
    """
    The main purpose of this function is to take a string containing digits and convert those digits into integers.
    It takes a string as the input. It splits the string into its 'digit' and 'other' components
    Taking every other item (starting with the second one, as the first is '') in the outcome of the split, the string
    format digits are converted to integers using the map() and int() functions.
    The numerical_convert function then returns any digits it found in 'value' in integer format.
    """
    split_value = file_name_compiler.split(value)
    split_value[1::2] = map(int, split_value[1::2])
    return split_value

# the following code loops through all 241 files in the directory 'genes'
# it then opens each one and searches between 'LOCUS' and '//' using the regexes
# then appends matched groups to the relevant list
# this is the method used for extracting all of the required data from the file

# -----------------------------------Parser function------------------------------------------------

def match_finder(list, compiler, else_statement = None):
    """
    This function essentially walks through a given directory taking the filenames, sorting by numerical name using
    the numerical_convert() function to convert string filenames into integers.
    It takes the following as parameters:
        list: the list to which the user wishes to append matches
        compiler: the regex compiler in the format re.compile(r"...()...") that the function uses to search for a match group.
        else_statement: this is a string that is appended to the list if no match group is found. It is set to None by default.
    If a match to the regex is found, match group 1 is appended to the list. If not, the else_statement is appended instead.
    Nothing visible is returned, but the list provided will be populated with matches.
    """
    for root, dirs, all_files in os.walk(indir):
        for infile in sorted(all_files, key=numerical_convert):
            open_file = open(os.path.join(root, infile), 'r')
            match = compiler.search(open_file.read())
            if match:
                list.append(str(match.group(1)))
            else:
                list.append(str(else_statement))
    return()

# --------------------------------------------------------------------------------------------------

genbank_accessions = []                                                      ## genbank accessions
accession_compiler = re.compile(r"^ACCESSION\s+(\w+).+\/\/", re.MULTILINE|re.DOTALL)
match_finder(genbank_accessions, accession_compiler, else_statement='none')

gene_ids = []                                                               ## gene IDs
id_compiler = re.compile(r"^LOCUS\s+(\w+).+\/\/", re.MULTILINE|re.DOTALL)
match_finder(gene_ids, id_compiler, else_statement='none')

gene_name = []
name_compiler = re.compile(r"^LOCUS\s.+\/gene\=\"(.+?)\".+\/\/", re.MULTILINE|re.DOTALL)
match_finder(gene_name, name_compiler, else_statement='none')

dna_seq = []
dnaseq_compiler = re.compile(r"^ORIGIN\s+(.+)\/\/", re.DOTALL|re.MULTILINE)
match_finder(dna_seq, dnaseq_compiler, else_statement='none')
clean_dna_seq = []                                                          ## DNA sequence
for x in dna_seq:
    sub1 = re.sub(r"\W", "", x)
    sub2 = re.sub(r"\d", "", sub1)
    clean_dna_seq.append(sub2)

gene_products = []                                                          ## 1st protein product
prod_compiler = re.compile(r"^LOCUS\s.+\/product\=\"(.+?)\".+\/\/", re.MULTILINE|re.DOTALL)
match_finder(gene_products, prod_compiler, else_statement='none')

chr_loc = []                                                                ## chromosomal location
chrloc_compiler = re.compile(r"^LOCUS\s.+\/map\=\"(.+?)\".+^\/\/", re.MULTILINE|re.DOTALL)
match_finder(chr_loc, chrloc_compiler, else_statement='15')

protein_seq = []
proseq_compiler = re.compile(r"^LOCUS\s.+\/translation\=\"(.+?)\".+\/\/", re.MULTILINE | re.DOTALL)
match_finder(protein_seq, proseq_compiler, else_statement='none')
clean_protein_seq = []                                                      ## protein sequence
for x in protein_seq:
    sub = re.sub(r"\W", "", x)
    clean_protein_seq.append(sub)
            
# --- extracting the coding seq of the gene in order to get the exon ranges --- #

cds_grab = []
for root, dirs, all_files in os.walk(indir):
    for infile in sorted(all_files, key=numerical_convert):
        open_file = open(os.path.join(root, infile), 'r')
        find_all_cds = list(re.findall(r"^\s{5}CDS\s+(.+?)\/", open_file.read(), re.MULTILINE | re.DOTALL))
        cds_grab.append(find_all_cds)

#for number, letter in enumerate(cds_grab):
    #print(number, letter)
#for number, letter in enumerate(gene_ids):
    #print(number, letter)

# this removes the \n and whitespace from the strings in cds_grab
# it leaves me with an overall list (cds_ws_strip), within which there are sub-lists
# the items in the sub-lists are all the coding seqs for 1 gene
cds_ws_strip = []
for list in cds_grab:
    subL = []
    for item in list:
        stripped_item = re.sub(r"\n\s{21}", "", item)
        subL.append(stripped_item)
    cds_ws_strip.append(subL)

#for number, letter in enumerate(cds_ws_strip):
    #print(number, letter)
#for number, letter in enumerate(gene_ids):
    #print(number, letter)

# the following code strips off superfluous characters from items in cds_ws_strip:
clean_boundaries = []
for list in cds_ws_strip:
    subL = []
    for item in list:
        b_sub = re.sub(r"join\(", "", item)
        sub1 = re.sub(r"\<", "", b_sub)
        sub2 = re.sub(r"\>", "", sub1)
        sub3 = re.sub(r"\(", "", sub2)
        sub4 = re.sub(r"\)", "", sub3)
        sub5 = re.sub(r"complement", "", sub4)
        subL.append(sub5)
    clean_boundaries.append(subL)

#for number, letter in enumerate(clean_boundaries):
    #print(number, letter)
#161 ['104..149,437..517', '926..996']

split_items = []
character = ','
for list in clean_boundaries:
    subL = []
    for item in list:
        if character in item:
            break_items = item.split(',')
            for component in break_items:
                subL.append(component)
        else:
            subL.append(item)
    split_items.append(subL)

#for number, letter in enumerate(split_items):
    #print(number, letter)
#221 ['U59692.1:2089..2187', 'U59693.1:710..809', 'U59693.1:1858..2093', 'U59693.1:2465..4329', '344..1028']

# the following code identifies any exons in the cds of loci which have labels from other loci - it then
# appends 'exons span multiple genes' to the end of each loci's list to indicate this, and chops off all but
# the last term, which is this phrase.
exon_across_genes_compiler = re.compile(r"[A-Z]{1,2}.+?\:")
remove_spans = []
phrase = 'exons span multiple genes'
for list in split_items:
    for item in list:
        match = exon_across_genes_compiler.search(item)
        if match:
            list.append(phrase)
    if phrase in list:
        l = len(list)
        chop = l - 1
        new_list = list[chop:]
        remove_spans.append(new_list)
    else:
        remove_spans.append(list)

#for number, letter in enumerate(remove_spans):
    #print(number, letter)
#233 ['1014..1226', '1379..1552', '2926..3022', '3152..3335', '5267..5404', '5478..5597',
#     '5801..5923', '6053..6239', '6361..6444', '6940..7149', '7511..7633', '8015..8068',
#     '8663..8781', '9056..9150', '9247..9370', '9610..9767', '9892..10014', '11372..11514']

# --- separating the start and end positions of the exons into an exon start list and an exon end list --- #

# the following code grabs all the exon start positions for a particular and puts them into a sub-list
# the sub-list is then appended to the main list:
exon_start = []
exon_end = []

for list in remove_spans:
    subL = []
    if phrase in list:
        exon_start.append(list)
    else:
        for item in list:
            match = re.findall(r"^(\d+)\.", item)
            if match:
                for x in match:
                    subL.append(x)
            else:
                subL.append('none')
        exon_start.append(subL)

#for number, letter in enumerate(exon_start):
    #print(number, letter)

for list in remove_spans:
    subL = []
    if phrase in list:
        exon_end.append(list)
    else:
        for item in list:
            match = re.findall(r"^\d+\.\.(\d+)", item)
            if match:
                for x in match:
                    subL.append(x)
            else:
                subL.append('none')
        exon_end.append(subL)

#for number, letter in enumerate(exon_start):
    #print(number, letter)
#for number, letter in enumerate(exon_end):
    #print(number, letter)

# -- Generating dictionaries that store gene_ids and exon start and end points -- #
dic1 = dict(zip(gene_ids, exon_start))
dic2 = dict(zip(gene_ids, exon_end))
dic1_dic2_list = [dic1, dic2]
dict_exon_boundaries = {}

#building a dictionary of exon start and end points with their corresponding keys
for key in (dic1.keys() | dic2.keys()):
    if key in dic1: dict_exon_boundaries.setdefault(key, []).append(dic1[key])
    if key in dic2: dict_exon_boundaries.setdefault(key, []).append(dic2[key])
splice_variant_compiler = re.compile(r"^.{7}S|.{8}S|.{9}S")

#removing splice variants
no_splice_dict = {}
for k,v in dict_exon_boundaries.items():
    match = splice_variant_compiler.search(k)
    if match:
        pass
    else:
        no_splice_dict[k] = v

#test
#b = no_splice_dict["JN245913"]
#spliced = no_splice_dict["AH008469S12"]
#print(spliced)
    #KeyError: 'AH008469S12'

# --------------------------------------------------------------------------------------------------
# -----------------------------------Database connection tier---------------------------------------

# Using Pandas to generate dataframes from my lists

#gene_ids                          will be 'Gene_ID' in DB
#chr_loc                           will be 'Chromosome_location' in DB
#clean_dna_seq                     will be 'DNA_sequence' in DB
#clean_protein_seq                 will be 'Protein_sequence' in DB
#gene_products                     will be 'Protein_product' in DB
#exon_start                        will be 'Start_location' in DB
#exon_end                          will be 'End_location' in DB

coding_region_df = pd.DataFrame.from_dict(no_splice_dict, orient='index', dtype=None)

gene_info_df = pd.DataFrame({'Gene_ID': gene_ids, 'Chromosome_location':chr_loc, 'DNA_sequence':clean_dna_seq,
                             'Protein_sequence':clean_protein_seq, 'Protein_product':gene_products}, index=gene_ids)
#coding_region_df = pd.DataFrame({'Gene_ID': gene_ids, 'End_location':str_ex_end, 'Start_location':str_ex_start},
#                                index=gene_ids)

engine = create_engine('mysql+mysqlconnector://root:pw@localhost:3306/biocomp_project', echo=False)


new_df = coding_region_df.stack()


# col1: 0 - key (gene id)
# col2: 1 - value (list)


# Porting to the database:
#gene_info_df.to_sql(name='Gene_info', con=engine, if_exists = 'append', index=False)
#coding_region_df.to_sql(name='Coding_region', con=engine, if_exists = 'append', index=False)

# ---------------------------------------------------------------------------------------------------
# -----------------------------------Testing tier----------------------------------------------------
"""
#testing lists - all should be 241 to align correct data values:
correct_length = 241
list_lengths = [len(genbank_accessions), len(gene_ids), len(clean_dna_seq), len(chr_loc),
                len(clean_protein_seq), len(gene_products), len(str_ex_start), len(str_ex_end)]
for list in list_lengths:
    if list != correct_length:
        print('test fail')
    else:
        print('length:', list, '--', 'test successful')
"""
