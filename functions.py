#! /usr/bin/env python3

from config import codons, codon_table, AA, enzyme_dict
import accessdata as ad
import scipy.stats as stats
import pandas as pd


def get_CDS_seq(DNA: str, CDS_loc: list):
    '''
    Return coding sequence from DNA and coding locations
    :param DNA: DNA sequence
    :type DNA: str
    :param CDS_loc: locations of starts and ends of coding regions
    :type CDS_loc: list of (int, int)
    :return: coding sequence
    :rtype: str

    >>> get_CDS_seq('TTTAAA',[(3,5)])
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
        codon = CDS[i:i+3]
        codonCount[codons.index(codon)] += 1
    return codonCount

# returns frequency of each codon as a percentage of the total number of codons
def codon_percent(CDS):
    count = count_codon_usage(CDS)
    total = sum(count)
    percent = [c/total for c in count]
    return percent

def codon_significance(CDS_length, gene_percent, chr_percent):
    pvalues = []
    padj = []
    for i in range(0,64):
        n = CDS_length / 3
        x = gene_percent[i] * n
        p = chr_percent[i]
        #cdf = stats.binom.cdf(x,n,p)
        pval = stats.binom_test(x,n,p)
        #p = 1-abs(0.5-cdf)*2
        pvaladj = round(pval*64,5) # Bonferroni correction
        pval = round(pval,5)
        pvalues.append(pval)
        padj.append(pvaladj)
    return pvalues, padj


def get_codon_table(CDS):
    '''
    return table of codons, their frequencies and their relative frequences
    :param CDS: Coding sequence
    :return:
    '''
    gene_percent = codon_percent(CDS)
    chr_percent = codon_table[1]
    rel_freq = [g/c for g,c in zip(gene_percent, chr_percent)]
    pval, padj = codon_significance(len(CDS), gene_percent, chr_percent)
    return [codons, AA, gene_percent, chr_percent, rel_freq, pval, padj]


# returns table with enyzmes and cutting locations
def getCuttingLocs(enzymeDict, DNA):
    cuttingLocs = []
    enzymes = []
    for enzyme in enzymeDict:
        seq = enzymeDict[enzyme]
        i = 0
        enzymeCuts = []     # Cutting locations for a single enzyme
        while DNA.find(seq,i) != -1:
            i = DNA.find(seq,i) + 1
            enzymeCuts.append(i-1) # Cutting location given by index
        cuttingLocs.append(enzymeCuts)
        enzymes.append(enzyme)
    return [enzymes,cuttingLocs]



def goodOrBadEnzyme(cutting_locs, CDS_locs):  # enzymeTable = [enzymes, cuttingLocs]
    cds_start = CDS_locs[0][0]
    cds_end = CDS_locs[len(CDS_locs) - 1][1]
    if all(cds_end < c or c < cds_start for c in cutting_locs):
        return 'Good'
    else:
        return 'Bad'

def getEnzymeTable(DNA, CDS_locs):
    '''

    :param DNA:
    :param CDS_locs:
    :return:
    '''
    enzymeTable = getCuttingLocs(enzyme_dict, DNA)
    enzymeQual = [goodOrBadEnzyme(cutting_locs, CDS_locs) for cutting_locs in enzymeTable[1]]
    enzymeTable.append(enzymeQual)
    return enzymeTable


def get_data(input, type):
    """
    :param input:
    :param type:
    :return: list containing:
        - DNA
        - locations of exon boundaries
        - codon table
        - enzyme table
    """
    [DNA, CDS_locs] = ad.get_DNA_and_CDS_from_SQL(input, type) #From accessdata module
    CDS = get_CDS_seq(DNA, CDS_locs)
    codonTable = get_codon_table(CDS)
    enzymeTable = getEnzymeTable(DNA, CDS_locs)
    return [DNA,CDS_locs,codonTable,enzymeTable]

'''testCDS = 'TTTTTTTTTAGAGAGAATCCTACTCTCTAAGCTTCGCGCGAAGCTCGCGCGC' \
          'GATAGCGCATAGCGCTAGCTATCAGCGGGGCGCCCGCGCCTCCTATATATATTCATTCTAGGAGGCTTCTTAAAGCT'
codon_table = pd.DataFrame(getCodonTable(testCDS)).T

print(get_data('AB024537','Gene_ID'))'''

if __name__ == "__main__":
    import doctest
    doctest.testmod()
