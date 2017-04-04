import functions
import accessdata
import pandas as pd

''' Script to calculate codon usage in the whole of Chromosome 15'''

def overallCodonUse():
    codonUse = [0]*64
    conn = accessdata.connectdb()
    cursor = conn.cursor()
    SQL = "SELECT gene_id FROM gene"
    cursor.execute(SQL)
    genes = cursor.fetchall()
    cursor.close()
    for gene in genes:
        SQL = "SELECT DNA FROM gene WHERE gene.gene_id='" + gene[0] +"';"
        cursor.execute(SQL)
        DNA = cursor.fetchone()
        SQL = "SELECT start_loc, end_loc FROM coding_region cr WHERE cr.gene_id = '" + gene[0] + "';"
        cursor.execute(SQL)
        CDSloc = cursor.fetchall()
        CDS = functions.get_CDS_seq(DNA, CDSloc)
        codonUse += functions.count_codon_usage(CDS)
    return codonUse

def overallCodonPercent():
    count = overallCodonUse()
    total = sum(count)
    percent = [c/total for c in count]
    return percent

############################################################


# CREATE SUMMARY TABLE FOR HOME PAGE
def summary_html_table():
    all_genes = accessdata.get_all_genes()
    df = pd.DataFrame(list(all_genes))
    df.columns = ['A', 'B', 'C', 'D', 'E']
    df = df[['A','B','E']]
    for col in df.columns:
        df[col] = df[col].apply(lambda x: '<a href=\"http://www.webcgiaddress.com/cgi-bin/cgi-script?type={0}&input={1}\">{1}</a>'.format(col,x))  # Link to summary page
    #df = df.set_index(['A'])
    pd.set_option('display.max_colwidth', 1000)
    df.to_html('summarytable.html',escape=False,index=False)

summary_html_table()
