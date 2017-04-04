for root, dirs, all_files in os.walk(indir):
    for infile in sorted(all_files, key=numerical_sort):
        open_file = open(os.path.join(root, infile), 'r')
        match_acc = accession_compiler.search(open_file.read())
        if match_acc:
            genbank_accessions.append(str(match_acc.group(1)))
        else:
            genbank_accessions.append(str('none'))

for root, dirs, all_files in os.walk(indir):
    for infile in sorted(all_files, key=numerical_sort):
        open_file = open(os.path.join(root, infile), 'r')
        match_id = id_compiler.search(open_file.read())
        if match_id:
            gene_ids.append(str(match_id.group(1)))
        else:
           gene_ids.append(str('none'))

for root, dirs, all_files in os.walk(indir):
    for infile in sorted(all_files, key=numerical_sort):
        open_file = open(os.path.join(root, infile), 'r')
        match_seq = dnaseq_compiler.search(open_file.read())
        if match_seq:
            dna_seq.append(str(match_seq.group(1)))
        else:
            dna_seq.append(str('none'))

for root, dirs, all_files in os.walk(indir):
    for infile in sorted(all_files, key=numerical_sort):
        open_file = open(os.path.join(root, infile), 'r')
        match_pp = prod_compiler.search(open_file.read())
        if match_pp:
            gene_products.append(str(match_pp.group(1)))
        else:
            gene_products.append(str('none'))

for root, dirs, all_files in os.walk(indir):
    for infile in sorted(all_files, key=numerical_sort):
        open_file = open(os.path.join(root, infile), 'r')
        match_chrloc = chrloc_compiler.search(open_file.read())
        if match_chrloc:
            chr_loc.append(str(match_chrloc.group(1)))
        else:
            chr_loc.append(chromosome_no)

for root, dirs, all_files in os.walk(indir):
    for infile in sorted(all_files, key=numerical_sort):
        open_file = open(os.path.join(root, infile), 'r')
        match_protseq = proseq_compiler.search(open_file.read())
        if match_protseq:
            protein_seq.append(str(match_protseq.group(1)))
        else:
            protein_seq.append(str('none'))


for root, dirs, all_files in os.walk(indir):
    for infile in sorted(all_files, key=numerical_sort):
        open_file = open(os.path.join(root, infile), 'r')
        match_cds = cds_compiler.search(open_file.read())
        if match_cds:
            ex_int_boundaries.append(match_cds.group(1))
        else:
            ex_int_boundaries.append('none')


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


# the following code generates a list (exons into lists)
# some lists just have one, whereas others have multiple exons, and so have lists containing multiple terms:
exons_into_lists = []
for list in split_items:
    subL = []
    for sublist in list:
        split_to_list = item.split(',')
        subL.append(split_to_list)
    exons_into_lists.append(subL)
print(exons_into_lists)
for number, letter in enumerate(exons_into_lists):
    print(number, letter)

#to remove the dots
remove_dots = []
for list in remove_spans:
    subL = []
    if phrase not in list:
        for item in list:
            no_dot = re.sub(r"\.\.", " ",item)
            subL.append(no_dot)
    remove_dots.append(subL)

for number, letter in enumerate(remove_dots):
    print(number, letter)

# -- Generating dictionaries that store gene_ids and exon start and end points -- #
dic1 = dict(zip(gene_ids, str(exon_start)))
dic2 = dict(zip(gene_ids, str(exon_end)))
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





"""
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
"""
#for number, letter in enumerate(exon_start):
    #print(number, letter)
#for number, letter in enumerate(exon_end):
    #print(number, letter)

exon_start_ls_s = [' '.join(x) for x in exon_start] #generating lists of strings
exon_end_ls_s = [' '.join(x) for x in exon_end]
print(exon_start_ls_s[:5])
print(exon_end_ls_s[:5])