#! /usr/bin/env python3

from functions import get_data
import cgi
import cgitb; cgitb.enable()
import pandas as pd


html = "Content-Type: text/html\n"
html += '''
<html>
<head>
 <title>Hello World!</title>
</head>
<body>
'''

"""
form = cgi.FieldStorage()

input = form['input'].value
type = form['type'].value"""

[DNA,CDS_loc,codon_table,enzyme_table] = get_data('AB024537', 'Gene_ID')


codon_table_df = pd.DataFrame(codon_table).T
codon_table_df.columns = ['Triplet', 'Amino Acid', 'Gene %', 'Chr %', 'Relative Frequency', 'P-value']
index = pd.MultiIndex.from_product([['T','C','A','G'],['T','C','A','G'],['T','C','A','G']])
codon_table_df = codon_table_df.set_index(index)
codon_table_df = codon_table_df.stack().unstack(level=-4).unstack()
'''for col in codon_table_df.columns:
    codon_table_df[col] = codon_table_df[col].apply(lambda x: x + col)
                                                    #'<a href= webcgiaddress?type='+col+'&input='+x+'/>' + x) # Link to summary page''' # I think this shouldn't be here

codon_table_html = codon_table_df.to_html(border=0)

enzyme_table_df = pd.DataFrame(enzyme_table).T
enzyme_table_df.columns = ['Enzyme','Cutting Locations','Good or Bad']

html += DNA
html += pd.DataFrame(CDS_loc,columns=['Start of coding region','End of coding region']).to_html(index=False)
html += codon_table_html
html += enzyme_table_df.to_html(index=False)

with open('test.html','w') as f:
    f.write(html)
'''
<body>
<h1>Hello World!</h1>
</body>
</html>
'''