import pymysql

from dbconfig import dbhost,dbuser,dbname,dbpass,dbport


def connectdb():
    conn = pymysql.connect(host=dbhost, port=dbport, user=dbuser, passwd = dbpass, db = dbname)
    return conn

def getDNAfromSQL(input, type, cursor):
    """
    returns DNA sequence for gene
    
    :param input: string
    :param type: "Gene_ID", "Gene_name", "Protein_product" or "Chromosome_location"
    :param cursor: 
    :return: string
    """
    query = "SELECT DNA_sequence FROM Gene_info WHERE " + type + " = '" + input + "';"
    cursor.execute(query)
    DNA = cursor.fetchone()[0]
    DNA = DNA.upper()
    return DNA

def getCDSfromSQL(input, type, cursor):
    """
    returns location of coding regions for gene

    :param input: string
    :param type: "Gene_ID", "Gene_name", "Protein_product" or "Chromosome_location"
    :param cursor: 
    :return: list of length 2 lists e.g. [[1,13],[15,17],[24,43]]
    """
    query = "SELECT Start_location, End_location FROM Coding_region cr, Gene_info g " \
            "WHERE cr.Gene_ID = g.Gene_ID " \
            "AND g." + type + " = '" + input + "';"
    cursor.execute(query)
    CDSloc = cursor.fetchall()
    CDSloc = [[int(x) for x in i] for i in CDSloc]
    return CDSloc


def get_DNA_and_CDS_from_SQL(input, type):
    """
    returns location of coding regions and dna sequence for gene

    :param input: string
    :param type: "Gene_ID", "Gene_name", "Protein_product" or "Chromosome_location"
    :param cursor: 
    :return: [DNA (string), CodingLocations ([[a1,b1],...,[an,bn]])
    """
    conn = connectdb()
    cursor = conn.cursor()
    DNA = getDNAfromSQL(input, type, cursor)
    CDSloc = getCDSfromSQL(input, type, cursor)
    cursor.close()
    conn.close()
    return [DNA,CDSloc]


def get_all_genes():
    conn = connectdb()
    cursor = conn.cursor()
    SQL = "SELECT * FROM Gene_info;"
    cursor.execute(SQL)
    rows = cursor.fetchall()
    cursor.close()
    return(rows)
