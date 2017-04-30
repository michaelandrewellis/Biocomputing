import pymysql

from dbconfig import dbhost,dbuser,dbname,dbpass,dbport


def connectdb():
    conn = pymysql.connect(host=dbhost, port=dbport, user=dbuser, passwd = dbpass, db = dbname)
    return conn

def getDNAfromSQL(input, type, cursor):
    query = "SELECT DNA_sequence FROM Gene_info WHERE " + type + " = '" + input + "';"
    cursor.execute(query)
    DNA = cursor.fetchone()[0]
    DNA = DNA.upper()
    return DNA

def getCDSfromSQL(input, type, cursor):
    query = "SELECT Start_location, End_location FROM Coding_region cr, Gene_info g " \
            "WHERE cr.Gene_ID = g.Gene_ID " \
            "AND g." + type + " = '" + input + "';"
    cursor.execute(query)
    CDSloc = cursor.fetchall()
    # Extra code to deal with database storing coding region locations as strings of lists of strings
    #CDSloc = CDSloc[0]
    #CDSloc = (ast.literal_eval(x) for x in CDSloc)
    #CDSloc = list(map(list, zip(*CDSloc)))
    CDSloc = [[int(x) for x in i] for i in CDSloc]

    return CDSloc


def get_DNA_and_CDS_from_SQL(input, type):
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
