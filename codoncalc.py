import functions
import accessdata

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
        codonUse += functions.countCodonUsage(CDS)
    return codonUse

def overallCodonPercent():
    count = overallCodonUse()
    total = sum(count)
    percent = [c/total for c in count]
    return percent

############################################################
