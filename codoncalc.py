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
    conn = accessdata.connectdb()
    cursor = conn.cursor()
    SQL = "SELECT * FROM gene"
    cursor.execute(SQL)
    rows = cursor.fetchall()
    cursor.close()
    df = pd.DataFrame(rows)
    df.columns = ['A','B','C','D']
    for col in df.columns:
        df[col] = df[col].apply(lambda x: '<a href= webcgiaddress?type = ' + col + '&input=' + x + '/>' + x)  # Link to summary page
    return(df.to_html)
