#! /usr/bin/env python3

import scipy.stats as stats
from config import codons, codon_table, AA, enzyme_dict

import accessdata as ad


def get_CDS_seq(DNA, CDS_loc):
    '''
    Return coding sequence from DNA and coding locations
    
    :param DNA: DNA sequence  
    :type DNA: str  
    :param CDS_loc: locations of starts and ends of coding regions  
    :type CDS_loc: list of (int, int)  
    :return: coding sequence  
    :rtype: str  

    >>> get_CDS_seq('TTTAAA', [(3,5)])  
    'TAA'
    '''
    CDS = ""
    for tuple in CDS_loc:
        CDS += DNA[tuple[0]-1:tuple[1]]         # Add each coding region
    return CDS


def count_codon_usage(CDS):
    '''
    Return codon frequency of a coding sequence.

    :param CDS: coding sequence
    :type CDS: str
    :return: codon frequencies
    :rtype: list

    >>> count_codon_usage('TTT')[0]  
    1
    '''
    codonCount = [0]*64
    for i in range(0,len(CDS),3):
        if len(CDS)-i >= 2: # Lengths of some sequences are not multiples of 3
            codon = CDS[i:i+3]
            codonCount[codons.index(codon)] += 1
    return codonCount


def codon_percent(CDS):
    """
    returns frequency of each codon as a percentage of the total number of codons

    :param CDS: coding sequence
    :type CDS: str
    :return: codon percentages within coding region
    :rtype: list of floats
    """
    count = count_codon_usage(CDS)
    total = sum(count)
    if total !=0:
        percent = [c/total for c in count] # Avoids a divide by zero error for entries that are missing a coding region
    else:
        percent = [0]*64
    return percent


def codon_significance(CDS_length, gene_percent, chr_percent):
    """
    returns p-value and adjusted p-value (Bonferroni correction) for the frequency of each codon using a two-tailed
    binomial test.

    :param CDS_length: length of coding region - should be a multiple of 3
    :type CDS_length: int
    :param gene_percent: percentage of each codon in the coding sequence
    :type gene_percent: list of floats
    :param chr_percent: percentage of each codon in chromosome 15
    :type chr_percent: list of floats
    :return: p-values and adjusted p-values
    :rtype: two lists
    """
    pvalues = []
    padj = []
    for i in range(0,64):
        n = CDS_length / 3
        x = gene_percent[i] * n
        p = chr_percent[i]
        pval = stats.binom_test(x,n,p)
        pvaladj = round(pval*64,5)  # Bonferroni correction
        pval = round(pval,5)
        pvalues.append(pval)
        padj.append(pvaladj)
    return pvalues, padj


def get_codon_table(CDS):
    """
    returns table of codons, their frequencies within the gene and chromosome, their relative frequencies, and their
    p-values.
    :param CDS: Coding sequence
    :type CDS: str
    :return:
    """
    gene_percent = codon_percent(CDS)
    chr_percent = codon_table[1]
    rel_freq = [g/c for g,c in zip(gene_percent, chr_percent)]
    pval, padj = codon_significance(len(CDS), gene_percent, chr_percent)
    return [codons, AA, gene_percent, chr_percent, rel_freq, pval, padj]


# returns table with enyzmes and cutting locations
def get_cutting_locs(enzyme_dict, DNA):
    """
    returns table with points at which the enzymes cut the DNA sequence

    :param enzyme_dict: names of the enzymes and the sequences on which they cut
    :type enzyme_dict: dictionary
    :param DNA: DNA sequence
    :type DNA: str
    :return: table of enzymes and their cutting locations
    :rtype: table
    """
    cutting_locs = []
    enzymes = []
    for enzyme in enzyme_dict:
        seq = enzyme_dict[enzyme]
        i = 0
        enzyme_cuts = []
        while DNA.find(seq,i) != -1:    # find(seq,i) = -1  when there are no more matches
            i = DNA.find(seq,i) + 1
            enzyme_cuts.append(i-1) # Cutting location given by index
        cutting_locs.append(enzyme_cuts)
        enzymes.append(enzyme)
    return [enzymes,cutting_locs]



def good_or_bad_enzyme(cutting_locs, CDS_locs):
    """
    Labels an enzyme "good" if it only cuts before the first coding region and after the last. Otherwise, labels an enzyme "bad".
    
    :param cutting_locs: locations at which enzyme cuts
    :type cutting_locs: list of int
    :param CDS_locs: locations of starts and ends of coding regions
    :type CDS_locs: list of 2-tuples
    :return: 'Good' or 'Bad'
    """
    cds_start = CDS_locs[0][0]      # start of first coding region
    cds_end = CDS_locs[len(CDS_locs) - 1][1]    # end of last coding region
    if all(cds_end < c or c < cds_start for c in cutting_locs) and cutting_locs:    # cutting_locs will be considered True if non-empty
        return 'Good'
    else:
        return 'Bad'

def get_enzyme_table(DNA, CDS_locs):
    """
    Return a table containing restriction enzymes, where they cut and whether they are "good" or "bad"

    :param DNA: DNA sequence
    :param CDS_locs: Starts and ends of coding regions
    :return: Enzyme table
    """
    enzymeTable = get_cutting_locs(enzyme_dict, DNA)
    enzymeQual = [good_or_bad_enzyme(cutting_locs, CDS_locs) for cutting_locs in enzymeTable[1]]
    enzymeTable.append(enzymeQual)
    return enzymeTable


def get_data(input, type):
    """
    returns the summary data for a gene
    
    :param input: string
    :param type: Either "Gene_ID", "Gene_name", "Protein_product" or "Chromosome_location"
    :return: list containing:
        - DNA
        - locations of exon boundaries
        - codon table
        - enzyme table
    """
    [DNA, CDS_locs] = ad.get_DNA_and_CDS_from_SQL(input, type) #From accessdata module
    CDS = get_CDS_seq(DNA, CDS_locs)
    codonTable = get_codon_table(CDS)
    enzymeTable = get_enzyme_table(DNA, CDS_locs)
    return [DNA,CDS_locs,codonTable,enzymeTable]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
