#! /usr/bin/env python3

from functions import get_data
import cgi
import cgitb; cgitb.enable()
import pandas as pd
import htmlfunctions


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

def codon_table_to_html(codon_table):
    codon_table_df = pd.DataFrame(codon_table).T
    codon_table_df.columns = ['Triplet', 'Amino Acid', 'Gene %', 'Chr %', 'Relative Frequency', 'P-value']
    index = pd.MultiIndex.from_product([['T','C','A','G'],['T','C','A','G'],['T','C','A','G']], names=['Second','First','Third'])
    codon_table_df = codon_table_df.set_index(index)
    codon_table_df = codon_table_df.stack().unstack(level=-4).unstack()
    codon_table_df = codon_table_df[codon_table_df.columns.set_levels(['T', 'C','A','G'], level=0)]
    index2 = pd.MultiIndex.from_product([['T','C','A','G'],['T','C','A','G']],names=['First','Third'])
    codon_table_df = codon_table_df.reindex(index2)
    return codon_table_df.to_html(border=1)

'''for col in codon_table_df.columns:
    codon_table_df[col] = codon_table_df[col].apply(lambda x: x + col)
                                                    #'<a href= webcgiaddress?type='+col+'&input='+x+'/>' + x) # Link to summary page''' # I think this shouldn't be here


codon_table_html = codon_table_to_html(codon_table)
enzyme_table_df = pd.DataFrame(enzyme_table).T
enzyme_table_df.columns = ['Enzyme','Cutting Locations','Good or Bad']


# ADD HIGHLIGHT REGIONS
opening_tag =  '<mark>' #'<span class=\"highlight\">'
closing_tag =  '</mark>' #'</span>'
j=0
tagged_DNA = ''
for i in CDS_loc:
    tagged_DNA += DNA[j:i[0]] + opening_tag + DNA[i[0]:i[1]+1] + closing_tag
    j=i[1]+1
tagged_DNA += DNA[j:]

#DNA_split = [tagged_DNA[i:i+100] for i in range(0, len(tagged_DNA), 100)]
DNA_html =  '<div class=\"DNA\"><code>'+tagged_DNA+'</code></div>' #'<div><code>'+'\n'.join(DNA_split)+'</code></div>'

html += pd.DataFrame(CDS_loc,columns=['Start of coding region','End of coding region']).to_html(index=False)
html += codon_table_html
html += enzyme_table_df.to_html(index=False)

htmlfunctions.draw_gene(DNA,CDS_loc,enzyme_table)

html += "<img src='TEST.png'/>"
html += DNA_html

with open('test.html','w') as f:
    f.write(html)
'''
<body>
<h1>Hello World!</h1>
</body>
</html>
'''