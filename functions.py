#! /usr/bin/env python3

from config import codons, codonTable, AA, enzymeDict
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
def codonPercent(CDS):
    count = count_codon_usage(CDS)
    total = sum(count)
    percent = [c/total for c in count]
    return percent

def codonSignificance(CDSlength, genePercent, chrPercent):
    pvalues = []
    padj = []
    for i in range(0,64):
        n = CDSlength / 3
        x = genePercent[i]*n
        p = chrPercent[i]
        #cdf = stats.binom.cdf(x,n,p)
        pval = stats.binom_test(x,n,p)
        #p = 1-abs(0.5-cdf)*2
        pvaladj = round(pval*64,5) # Bonferroni correction
        pval = round(pval,5)
        if pval<0.05/64: # Bonferroni correction
            pass
        pvalues.append(pval)
        padj.append(pvaladj)
    return pvalues, padj

# returns table of codons, their frequencies and their relative frequences
def getCodonTable(CDS):   # TURN INTO DATAFRAME?
    genePercent = codonPercent(CDS)
    chrPercent = codonTable[1]
    relFreq = [g/c for g,c in zip(genePercent, chrPercent)]
    pval, padj = codonSignificance(len(CDS),genePercent,chrPercent)
    return [codons, AA, genePercent, chrPercent, relFreq, pval, padj]


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


# GOOD IF CUTS ANYWHERE OUTSIDE CODING REGION -  CHANGE THIS
def goodOrBadEnzyme(cuts, CDSlocs): # enzymeTable = [enzymes, cuttingLocs]
    CDSstart = CDSlocs[0][0]
    CDSend = CDSlocs[len(CDSlocs)-1][1]
    if any(CDSstart>c for c in cuts) and any(CDSend<c for c in cuts) and all(CDSend<c or c<CDSstart for c in cuts):
        return 'Good'
    else:
        return 'Bad'

def getEnzymeTable(DNA,CDSloc):
    '''

    :param DNA:
    :param CDSloc:
    :return:
    '''
    enzymeTable = getCuttingLocs(enzymeDict, DNA)
    enzymeQual = [goodOrBadEnzyme(x, CDSloc) for x in enzymeTable[1]]
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
    [DNA, CDSloc] = ad.get_DNA_and_CDS_from_SQL(input, type) #From accessdata module
    CDS = get_CDS_seq(DNA, CDSloc)
    codonTable = getCodonTable(CDS)
    enzymeTable = getEnzymeTable(DNA, CDSloc)
    return [DNA,CDSloc,codonTable,enzymeTable]

'''testCDS = 'TTTTTTTTTAGAGAGAATCCTACTCTCTAAGCTTCGCGCGAAGCTCGCGCGC' \
          'GATAGCGCATAGCGCTAGCTATCAGCGGGGCGCCCGCGCCTCCTATATATATTCATTCTAGGAGGCTTCTTAAAGCT'
codon_table = pd.DataFrame(getCodonTable(testCDS)).T

print(get_data('AB024537','Gene_ID'))'''

if __name__ == "__main__":
    import doctest
    doctest.testmod()
