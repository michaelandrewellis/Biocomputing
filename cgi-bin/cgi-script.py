#! /usr/bin/env python3

import functions
import cgi
import cgitb; cgitb.enable()
import pandas as pd
import htmlfunctions


html = "Content-Type: text/html\n"
html += '''
<html>
<head>
 <title>Summary Page</title>
</head>
<body>
'''

"""
form = cgi.FieldStorage()

input = form['input'].value
type = form['type'].value"""

[DNA,CDS_loc,codon_table,enzyme_table] = functions.get_data('AB024537', 'Gene_ID')


'''Possibly put in htmlfunctions.py'''
def codon_table_to_html(codon_table):
    codon_table_df = pd.DataFrame(codon_table).T
    codon_table_df.columns = ['Triplet', 'Amino Acid', 'Gene %', 'Chr %', 'Relative Frequency', 'p-value', 'p-value Adjusted']
    index = pd.MultiIndex.from_product([['T','C','A','G'],['T','C','A','G'],['T','C','A','G']], names=['Second','First','Third'])
    codon_table_df = codon_table_df.set_index(index)
    codon_table_df = codon_table_df.stack().unstack(level=-4).unstack()
    codon_table_df = codon_table_df[codon_table_df.columns.set_levels(['T', 'C','A','G'], level=0)]
    index2 = pd.MultiIndex.from_product([['T','C','A','G'],['T','C','A','G']],names=['First','Third'])
    codon_table_df = codon_table_df.reindex(index2)
    return codon_table_df.to_html(border=1)



codon_table_html = codon_table_to_html(codon_table)
colours = ['blue','yellow','pink']
enzyme_table_with_colour = enzyme_table + [colours]
enzyme_table_df = pd.DataFrame(enzyme_table_with_colour).T
enzyme_table_df.columns = ['Enzyme','Cutting Locations','Good or Bad', 'Colour']


# ADD HIGHLIGHT REGIONS
'''
opening_tag =  '<mark>'
closing_tag =  '</mark>'
j=0
tagged_DNA = ''
for i in CDS_loc:
    tagged_DNA += DNA[j:i[0]] + opening_tag + DNA[i[0]:i[1]+1] + closing_tag
    j=i[1]+1
tagged_DNA += DNA[j:]
'''
tagged_DNA = htmlfunctions.highlight_CDS(DNA,CDS_loc)
DNA_html =  '<div class=\"DNA\"><code>'+tagged_DNA+'</code></div>'

html += pd.DataFrame(CDS_loc,columns=['Start of coding region','End of coding region']).to_html(index=False)
html += codon_table_html
html += enzyme_table_df.to_html(index=False)

htmlfunctions.draw_gene(DNA,CDS_loc,enzyme_table)
html += "<img src='exons.png'/>"

html += DNA_html
html += "</body>"
html += "</html>"

with open('test.html','w') as f:
    f.write(html)
