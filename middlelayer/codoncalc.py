import ast

import middlelayer.accessdata as accessdata
import middlelayer.functions as functions
import pandas as pd

''' Script to calculate codon usage in the whole of Chromosome 15'''


def overallCodonUse():
    codonUse = [0]*64
    conn = accessdata.connectdb()
    cursor = conn.cursor()
    SQL = "SELECT Gene_ID FROM Gene_info"
    cursor.execute(SQL)
    genes = cursor.fetchall()
    for gene in genes:
        SQL = "SELECT DNA_sequence FROM Gene_info WHERE Gene_info.Gene_ID='" + gene[0] +"';"
        cursor.execute(SQL)
        DNA = cursor.fetchone()[0]
        DNA = DNA.upper()
        SQL = "SELECT Start_location, End_location FROM Coding_region cr WHERE cr.gene_id = '" + gene[0] + "';"
        cursor.execute(SQL)
        CDSloc = cursor.fetchall()
        CDSloc = [[int(i) for i in x] for x in CDSloc]
        print(CDSloc)
        ######################### EXTRA CODE TO DEAL WITH FORMAT
        '''
        CDSloc = CDSloc[0]
        if CDSloc[0] == 'exons span multiple genes':
            continue
        CDSloc = (ast.literal_eval(x) for x in CDSloc)
        print(CDSloc)
        CDSloc = list(map(list, zip(*CDSloc)))
        CDSloc = [[int(x) for x in i] for i in CDSloc]
        '''
        ####################################
        CDS = functions.get_CDS_seq(DNA, CDSloc)
        ######################################
        if len(CDS) % 3 != 0 or 'N' in CDS:
            continue
        #####################################
        codonUse = [a + b for a, b in zip(codonUse, functions.count_codon_usage(CDS))]
        #codonUse += functions.count_codon_usage(CDS)
    cursor.close()
    return codonUse

def overallCodonPercent():
    count = overallCodonUse()
    total = sum(count)
    percent = [c/total for c in count]
    return percent

############################################################

def summary_data_frame():
    all_genes = accessdata.get_all_genes()
    df = pd.DataFrame(list(all_genes))
    df.columns = ['Accession', 'Location', 'DNA', 'Amino Acid Sequence', 'Protein Product']
    df = df[df.DNA.str.contains("n") == False]  # Remove DNA containing 'n'
    df = addLocationCols(df)
    df.to_csv('summarytable.csv')

# CREATE SUMMARY TABLE FOR HOME PAGE
def summary_html_table():
    summary_data_frame()
    df = pd.DataFrame.from_csv('summarytable.csv')
    df = df[['Accession','Location','Protein Product']]
    df['Accession'] = df['Accession'].apply(
        lambda x: '<a href=\"http://www.webcgiaddress.com/cgi-bin/cgi-script?type={0}&input={1}\">{1}</a>'.format('Accession',x))
    
    #for col in df.columns:
        #df[col] = df[col].apply(lambda x: '<a href=\"http://www.webcgiaddress.com/cgi-bin/cgi-script?type={0}&input={1}\">{1}</a>'.format(col,x))  # Link to summary page
    #df = df.set_index(['A'])
    pd.set_option('display.max_colwidth', 1000)
    df.to_html('summarytable.html',escape=False,index=False)
    
def addLocationCols(df):
    df = pd.DataFrame.from_csv('summarytable.csv')
    df = df[df['Location'] != '15']
    df = df[df['Location'] != 'q']
    df = df[df['Location'].str.contains("between") == False]
    df = df[df['Location'].str.contains("ter") == False]
    df['Location'] = df['Location'].str.replace('15p','p')
    df['Location'] = df['Location'].str.replace('15q','q')
    df['Arm'] = df['Location'].str.extract('([pq])', expand = True)
    df['Start'] = df['Location'].str.extract('(?P<start>\d\d)', expand=True)
    df['End'] = df['Location'].str.extract('\d\d.*(?P<end>\d\d).*', expand=True)
    df['End'] = df['End'].fillna(df['Start'])
    return df

summary_html_table()
print(overallCodonPercent())


