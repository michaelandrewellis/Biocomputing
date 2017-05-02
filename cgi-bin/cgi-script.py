#!/usr/bin/env python3
""" 
Cgi script to generate either summary page for selected gene or a summary table of search matches
"""

import cgitb
cgitb.enable()
import cgi
import pandas as pd

import sys
sys.path.append('/d/user6/em001/WWW/')

import functions
import exondiagram

form = cgi.FieldStorage()

input_value = form['input'].value
input_type = form['type'].value


def codon_table_to_html(codon_table):
    codon_table_df = pd.DataFrame(codon_table).T
    codon_table_df.columns = ['Triplet', 'Amino Acid', 'Gene %', 'Chr %', 'Relative Frequency', 'p-value', 'p-value Adjusted']
    index = pd.MultiIndex.from_product([['T','C','A','G'],['T','C','A','G'],['T','C','A','G']], names=['Second','First','Third'])
    codon_table_df = codon_table_df.set_index(index)
    codon_table_df = codon_table_df.stack().unstack(level=-4).unstack()
    codon_table_df = codon_table_df[codon_table_df.columns.set_levels(['T', 'C','A','G'], level=0)]
    index2 = pd.MultiIndex.from_product([['T','C','A','G'],['T','C','A','G']],names=['First','Third'])
    codon_table_df = codon_table_df.reindex(index2)
    return codon_table_df.to_html(border=1, classes='codon_table')


def enzyme_table_to_html(enzyme_table_with_colour):
    enzyme_table_df = pd.DataFrame(enzyme_table_with_colour).T
    enzyme_table_df.columns = ['Enzyme', 'Cutting Locations', 'Good or Bad', 'Colour']
    return enzyme_table_df.to_html(classes='enzyme_table',index=False)


def highlight_CDS(DNA, CDS_locs):
    '''
    Add html tags to highlight the coding region of a DNA sequence
    :param DNA: DNA sequence
    :param CDS_locs: locations of starts and ends of coding regions
    :return: DNA sequence with '<mark>' and '</mark>' tags either side of coding regions
    '''
    opening_tag = '<mark>'
    closing_tag = '</mark>'
    j = 0
    tagged_DNA = ''
    for i in CDS_locs:
        tagged_DNA += DNA[j:i[0]] + opening_tag + DNA[i[0]:i[1] + 1] + closing_tag
        j = i[1] + 1
    tagged_DNA += DNA[j:]
    return tagged_DNA

def DNA_to_html(DNA, CDS_locs):
    """
    Returns DNA sequence as html with coding region highlighted

    :param DNA: DNA sequence
    :param CDS_locs: Starts and ends of coding regions
    :type CDS_locs: list of length two lists
    :return: html code for DNA sequence with tags to label and highlight
    """
    tagged_DNA = highlight_CDS(DNA, CDS_locs)
    DNA_html = '<div class=\"DNA\"><code>' + tagged_DNA + '</code></div>'
    return DNA_html


########################### THE SCRIPT TO PRODUCE THE WEB PAGE ########################################################

html = "Content-Type: text/html\n"

if input_type == 'Chromosome_location':
    df = pd.DataFrame.from_csv("../summarytable.csv")
    if 'p' in input_value:
        arm = 'p'
        position = input_value.replace('p','')
    elif 'q' in input_value:
        arm  = 'q'
        position = input_value.replace('q', '')
    df = df[df['Arm']==arm]
    df = df[df.Start <= position]
    df = df[df['End'] >= position]
    html = df[['Accession','Location','Protein Product']].to_html
elif input_type == 'Protein_product':
    df = pd.DataFrame.from_csv("../summarytable.csv")
    df = df[df['Protein Product']==input_value]
    html = df[['Accession','Location','Protein Product','Gene Name']].to_html
elif input_type == 'Gene_name':
    df = pd.DataFrame.from_csv("../summarytable.csv")
    df = df[df['Gene Name'] == input_value]
    html = df[['Accession', 'Location', 'Protein Product', 'Gene Name']].to_html
elif input_type == 'Gene_ID':
    [DNA, CDS_locs, codon_table, enzyme_table] = functions.get_data(input_value, 'Gene_ID')
    colours = ['Red', 'Yellow', 'Pink']
    enzyme_table_with_colour = enzyme_table + [colours]
    html += '''
    <html>
    <head>
     <title>Summary Page</title>
     <link rel="stylesheet" href="stylesheet.css">
    </head>
    <body>
    <h1>Summary Page for Gene</h1>
    '''
    html += pd.DataFrame(CDS_locs, columns=['Start of coding region','End of coding region']).\
        to_html(index=False,classes='CDS_table')
    html += codon_table_to_html(codon_table)
    html += enzyme_table_to_html(enzyme_table_with_colour)
    
    exondiagram.draw_gene(DNA, CDS_locs, enzyme_table_with_colour)
    
    html += "<img src='http://student.cryst.bbk.ac.uk/~em001/cgi-bin/exons.png'/>"
    html += DNA_to_html(DNA, CDS_locs)
    html += "</body>"
    html += "</html>"

print(html)
