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