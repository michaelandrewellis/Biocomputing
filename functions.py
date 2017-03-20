from config import codons, codonTable, AA, enzymeDict
import accessdata as ad
import scipy.stats as stats
import pandas as pd


# returns coding sequence from coding locations and DNA
def get_CDS_seq(DNA: str, CDS_loc: list):
    '''
    Return coding sequence for DNA sequence
    :param DNA: DNA sequence
    :type DNA: str
    :param CDS_loc: Locations of coding regions
    :type CDS_loc: list of (int, int)
    :return:
    '''
    CDS = ""
    for tuple in CDS_loc:
        CDS += DNA[tuple[0]-1:tuple[1]]         # Add each coding region
    return CDS

# returns list of codon counts
def countCodonUsage(CDS):
    codonCount = [0]*64
    for i in range(0,len(CDS),3):
        codon = CDS[i:i+3]
        codonCount[codons.index(codon)] += 1
    return codonCount

# returns frequency of each codon as a percentage of the total number of codons
def codonPercent(CDS):
    count = countCodonUsage(CDS)
    total = sum(count)
    percent = [c/total for c in count]
    return percent

def codonSignificance(CDSlength, genePercent, chrPercent):
    pvalues = []
    for i in range(0,64):
        n = CDSlength / 3
        x = genePercent[i]*n
        p = chrPercent[i]
        #cdf = stats.binom.cdf(x,n,p)
        pval = stats.binom_test(x,n,p)
        #p = 1-abs(0.5-cdf)*2
        pval = round(pval,3)
        if pval<0.05/64: # Bonferroni correction
            pval = str(pval)+'*'
        pvalues.append(pval)
    return pvalues

# returns table of codons, their frequencies and their relative frequences
def getCodonTable(CDS):
    genePercent = codonPercent(CDS)
    chrPercent = codonTable[1]
    relFreq = [g/c for g,c in zip(genePercent, chrPercent)]
    sig = codonSignificance(len(CDS),genePercent,chrPercent)
    return [codons, AA, genePercent, chrPercent, relFreq, sig]


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

# gets data for web page from database
def getData(input, type):
    '''

    :param input:
    :param type:
    :return:
    '''
    [DNA, CDSloc] = ad.get_DNA_and_CDS_from_SQL(input, type) #From accessdata module
    CDS = get_CDS_seq(DNA, CDSloc)
    codonTable = getCodonTable(CDS)
    enzymeTable = getEnzymeTable(DNA, CDSloc)
    return [DNA,CDSloc,codonTable,enzymeTable]

testCDS = 'TTTTTTTTTAGAGAGAATCCTACTCTCTAAGCTTCGCGCGAAGCTCGCGCGC' \
          'GATAGCGCATAGCGCTAGCTATCAGCGGGGCGCCCGCGCCTCCTATATATATTCATTCTAGGAGGCTTCTTAAAGCT'
print(pd.DataFrame(getCodonTable(testCDS)).T)

