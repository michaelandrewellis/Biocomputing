def genbank_parser(list, compiler, else_statement = None):
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

import os
import re
indir = '/Users/ainefairbrother/PycharmProjects/BiocomputingII/genes'

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

string = ('''LOCUS       JN245918                1025 bp    DNA     linear   PRI 28-DEC-2011
DEFINITION  Homo sapiens isolate B51 KIAA0101 (KIAA0101) gene, exons 1, 2, 4
            and partial cds.
ACCESSION   JN245918
VERSION     JN245918.1  GI:365753439
KEYWORDS    .
SOURCE      Homo sapiens (human)
  ORGANISM  Homo sapiens
            Eukaryota; Metazoa; Chordata; Craniata; Vertebrata; Euteleostomi;
            Mammalia; Eutheria; Euarchontoglires; Primates; Haplorrhini;
            Catarrhini; Hominidae; Homo.
REFERENCE   1  (bases 1 to 1025)
  AUTHORS   Jain,M., Zhang,L., Patterson,E.E. and Kebebew,E.
  TITLE     KIAA0101 Is Overexpressed, and Promotes Growth and Invasion in
            Adrenal Cancer
  JOURNAL   PLoS ONE 6 (11), E26866 (2011)
   PUBMED   22096502
  REMARK    Publication Status: Online-Only
REFERENCE   2  (bases 1 to 1025)
  AUTHORS   Jain,M., Zhang,L., Patterson,E. and Kebebew,E.
  TITLE     Direct Submission
  JOURNAL   Submitted (13-JUL-2011) Endocrine Oncology Section, Surgery Branch,
            National Institute of Health, 10-CRC - Hatfield Clinical Research
            Center, 4-5952, Bethesda, MD 20892, USA
FEATURES             Location/Qualifiers
     source          1..1025
                     /organism="Homo sapiens"
                     /mol_type="genomic DNA"
                     /isolate="B51"
                     /isolation_source="benign tumor"
                     /db_xref="taxon:9606"
                     /chromosome="15"
                     /map="15q23"
                     /tissue_type="adrenal gland"
     gene            1..1025
                     /gene="KIAA0101"
                     /gene_synonym="OEATC"
                     /gene_synonym="p15/PAF"
     mRNA            join(1..149,437..>517)
                     /gene="KIAA0101"
                     /gene_synonym="OEATC"
                     /gene_synonym="p15/PAF"
                     /product="KIAA0101"
     exon            1..149
                     /gene="KIAA0101"
                     /gene_synonym="OEATC"
                     /gene_synonym="p15/PAF"
                     /number=1
     CDS             join(104..149,437..>517)
                     /gene="KIAA0101"
                     /gene_synonym="OEATC"
                     /gene_synonym="p15/PAF"
                     /note="coding region disrupted by sequencing gap"
                     /codon_start=1
                     /product="KIAA0101"
                     /protein_id="AEW89524.1"
                     /db_xref="GI:365753440"
                     /translation="MVRTKADSVPGTYRKVVAARAPRKVLGSSTSATNSTSVSSRK"
     exon            437..517
                     /gene="KIAA0101"
                     /gene_synonym="OEATC"
                     /gene_synonym="p15/PAF"
                     /number=2
     gap             571..670
                     /estimated_length=unknown
     mRNA            <926..1025
                     /gene="KIAA0101"
                     /gene_synonym="OEATC"
                     /gene_synonym="p15/PAF"
                     /product="KIAA0101"
     exon            926..1025
                     /gene="KIAA0101"
                     /gene_synonym="OEATC"
                     /gene_synonym="p15/PAF"
                     /number=4
     CDS             <926..996
                     /gene="KIAA0101"
                     /gene_synonym="OEATC"
                     /gene_synonym="p15/PAF"
                     /note="coding region disrupted by sequencing gap"
                     /codon_start=3
                     /product="KIAA0101"
                     /protein_id="AEW89525.1"
                     /db_xref="GI:365753441"
                     /translation="HVLCNLITQMMKKNRTFSFIFE"
ORIGIN
        1 ccaatataaa ctgtggcggg atagttttcg ggtccttgtc cagtgaaaca ccctcggctg
       61 ggaagtcagt tcgttctctc ctctcctctc ttcttgtttg aacatggtgc ggactaaagc
      121 agacagtgtt ccaggcactt acagaaaagg tgaggcgatc gagtgtggta ctggagggcg
      181 ggggggtcct cccggcagcc tggccacggg cgacagacgc cagaggtccc cctgggccct
      241 gtgcgccaaa ctcatctagc tagccaggga gtagccgcct ggccccttta cctagaagag
      301 gaagtcgcag gggcagggta aggttatcct gctgttctgg atcgccaggc tctcctctcc
      361 aagctgctgg ggtccaggac tcggtgtcgg aaccctcctg ccccttctga acaccctttt
      421 ttgcctctct tcacagtggt ggctgctcga gcccccagaa aggtgcttgg ttcttccacc
      481 tctgccacta attcgacatc agtttcatcg aggaaaggta agaagagccc tcctaaagtt
      541 aggggatcag tcctggcacc tgcaagcccc nnnnnnnnnn nnnnnnnnnn nnnnnnnnnn
      601 nnnnnnnnnn nnnnnnnnnn nnnnnnnnnn nnnnnnnnnn nnnnnnnnnn nnnnnnnnnn
      661 nnnnnnnnnn tacaacgtag tctaaaggag aaacactgat tctgcaaatt aacaggcaaa
      721 taaattgtta aaaattttgt tgcattaata cttgaaattt gtaggtgttt gttaattaat
      781 gaagtttaat tttctttcat ttctagtcat tagaccagat ctactgcact gttaattaat
      841 gttcctgatt tatataggtt tgtaactatt tttttcaaac agttgatact tggatggcta
      901 ttgatgttct ctcttctttt cacagagcat gtcctttgca acctgatcac acaaatgatg
      961 aaaaagaata gaactttctc attcatcttt gaataacgtc tccttgttta ccctggtatt
     1021 ctaga
//''')


find_all_cds = re.findall(r"^\s{5}CDS\s+(.+?)\/", string, re.MULTILINE|re.DOTALL)

print(find_all_cds)
