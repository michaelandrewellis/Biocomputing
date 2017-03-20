import pymysql
from dbconfig import dbhost,dbuser,dbname,dbpass,dbport

def connectdb():
    conn = pymysql.connect(host=dbhost, port=dbport, user=dbuser, passwd = dbpass, db = dbname)
    return conn

def getDNAfromSQL(input, type, cursor):
    query = "SELECT DNA FROM gene WHERE " + type + " = '" + input + "';"
    cursor.execute(query)
    DNA = cursor.fetchone()
    return DNA

def getCDSfromSQL(input, type, cursor):
    query = "SELECT start_loc, end_loc FROM coding_region cr, gene " \
            "WHERE cr.gene_id = gene.geneid " \
            "AND gene." + type + " = '" + input + "';"
    cursor.execute(query)
    CDSloc = cursor.fetchall()
    return CDSloc


def get_DNA_and_CDS_from_SQL(input, type):
    conn = connectdb()
    cursor = conn.cursor()
    DNA = getDNAfromSQL(input, type, cursor)
    CDSloc = getCDSfromSQL(input, type, cursor)
    cursor.close()
    conn.close()
    return [DNA,CDSloc]
