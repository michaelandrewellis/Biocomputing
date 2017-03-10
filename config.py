# TEST CHANGE

codons = ['TTT', 'TTC', 'TTA', 'TTG',
          'CTT', 'CTC', 'CTA', 'CTG',
          'ATT', 'ATC', 'ATA', 'ATG',
          'GTT', 'GTC', 'GTA', 'GTG',
          'TCT', 'TCC', 'TCA', 'TCG',
          'CCT', 'CCC', 'CCA', 'CCG',
          'ACT', 'ACC', 'ACA', 'ACG',
          'GCT', 'GCC', 'GCA', 'GCG',
          'TAT', 'TAC', 'TAA', 'TAG',
          'CAT', 'CAC', 'CAA', 'CAG',
          'AAT', 'AAC', 'AAA', 'AAG',
          'GAT', 'GAC', 'GAA', 'GAG',
          'TGT', 'TGC', 'TGA', 'TGG',
          'CGT', 'CGC', 'CGA', 'CGG',
          'AGT', 'AGC', 'AGA', 'AGG',
          'GGT', 'GGT', 'GGA', 'GGG']

AA = ['Phe','Phe','Leu','Leu',
      'Leu','Leu','Leu','Leu',
      'Ile','Ile','Ile','Met',
      'Val','Val','Val','Val',
      'Ser','Ser','Ser','Ser',
      'Pro','Pro','Pro','Pro',
      'Thr','Thr','Thr','Thr',
      'Ala','Ala','Ala','Ala',
      'Tyr','Tyr','Stop codon','Stop codon',
      'His','His','Gln','Gln',
      'Asn','Asn','Lys','Lys',
      'Asp','Asp','Glu','Glu',
      'Cys','Cys','Stop codon', 'Trp',
      'Arg','Arg','Arg','Arg',
      'Ser','Ser','Arg','Arg',
      'Gly','Gly','Gly','Gly']


percent = [1/64]*64


codonTable = [codons,percent]

codons = ['TTT', 'TTC', 'TTA', 'TTG',
          'CTT', 'CTC', 'CTA', 'CTG',
          'ATT', 'ATC', 'ATA', 'ATG',
          'GTT', 'GTC', 'GTA', 'GTG',
          'TCT', 'TCC', 'TCA', 'TCG',
          'CCT', 'CCC', 'CCA', 'CCG',
          'ACT', 'ACC', 'ACA', 'ACG',
          'GCT', 'GCC', 'GCA', 'GCG',
          'TAT', 'TAC', 'TAA', 'TAG',
          'CAT', 'CAC', 'CAA', 'CAG',
          'AAT', 'AAC', 'AAA', 'AAG',
          'GAT', 'GAC', 'GAA', 'GAG',
          'TGT', 'TGC', 'TGA', 'TGG',
          'CGT', 'CGC', 'CGA', 'CGG',
          'AGT', 'AGC', 'AGA', 'AGG',
          'GGT', 'GGT', 'GGA', 'GGG']

enzymeDict = {'EcoRI':'GAATC',
              'BamHI':'GGATCC',
              'BsumMI':'CTCGAG'}