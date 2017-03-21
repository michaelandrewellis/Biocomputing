#! /usr/bin/env python3

from functions import get_data
import cgi
import cgitb; cgitb.enable()
import pandas as pd

''' PERHAPS ADD DEBUGGING '''

print ("Content-Type: text/html\n")
"""
form = cgi.FieldStorage()

input = form['input'].value
type = form['type'].value

[DNA,CDS_loc,codon_table,enzyme_table] = get_data('geneid', geneid)


codon_table_df = pd.DataFrame(codon_table).T
codon_table_df.columns = ['Triplet', 'Amino Acid', 'Gene %', 'Chr %', 'Relative Frequency', 'P-value']
index = pd.MultiIndex.from_product([['T','C','A','G'],['T','C','A','G'],['T','C','A','G']])
codon_table_df = codon_table_df.set_index(index)
codon_table_df = codon_table_df.stack().unstack(level=-4).unstack()
codon_table_html = codon_table_df.to_html


print(DNA)
print(pd.DataFrame(CDS_loc,columns=['Start of coding region','End of coding region']).to_html(index=False))
print(codon_table_html())
"""
print('''
<html>
<head>
 <title>Hello World!</title>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>
''')