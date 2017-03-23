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