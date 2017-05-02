"""
Module of functions used to generate elements for diagram of gene on summary page. 
"""

from PIL import Image, ImageDraw

# Parameters for exon diagram
image_height=50
image_width = 1000
v_midpoint = image_height/2
exon_height = 20
intron_height = 5
enzyme_marker_height = 40


def draw_intron(start,end,draw):
    '''
    Draw a rectangle to represent an intron
    :param start: horizontal position of first pixel of intron
    :param end: horizontal position of last pixel of intron
    :param draw: draw = PIL.ImageDraw.Draw(image) -- an object that can be used to draw in the given image
    :return: None
    '''
    x0 = start
    y0 = v_midpoint-intron_height/2
    x1 = end
    y1 = v_midpoint + intron_height/2
    draw.rectangle([x0,y0,x1,y1],fill='mediumblue')


def draw_exon(start,end,draw):
    '''
    Draw a rectangle to represent an exon
    :param start: horizontal position of first pixel of exon
    :param end: horizontal position of last pixel of exon
    :param draw: draw = PIL.ImageDraw.Draw(image) -- an object that can be used to draw in the given image
    :return: None
    '''
    x0 = start
    y0 = v_midpoint-exon_height/2
    x1 = end
    y1 = v_midpoint + exon_height/2
    draw.rectangle([x0,y0,x1,y1],fill='cornflowerblue')


def draw_enzyme(location,colour,draw):
    '''
    Draw an ellipse to represent the cutting point of an enzyme
    :param location: horizontal pixel position of cutting location on diagram
    :param colour: colour of ellipse
    :param draw: draw = PIL.ImageDraw.Draw(image) -- an object that can be used to draw in the given image
    :return: None
    '''
    x0 = location - enzyme_marker_height/8
    y0 = v_midpoint - enzyme_marker_height/2
    x1 = location + enzyme_marker_height/8
    y1 = v_midpoint + enzyme_marker_height/2
    draw.ellipse([x0,y0,x1,y1],fill=colour,outline = 'black')



def draw_gene(DNA,CDS_loc,enzyme_table_with_colour):
    '''
    Draw a diagram of a gene showing exons and enzyme cutting locations and save it to "exons.png"
    :param DNA: DNA sequence
    :param CDS_loc: locations of starts and ends of coding regions
    :param enzyme_table: table of [[cutting enzymes], [cutting locations], [good or bad enzyme], [colour]]
    :return: None
    '''
    im = Image.new("RGB", (image_width, image_height), "white")
    scale = image_width/len(DNA)
    draw = ImageDraw.Draw(im)
    draw_intron(0,len(DNA)*scale,draw)
    for i in CDS_loc:
        draw_exon(i[0]*scale,(i[1]+1)*scale,draw)
    for cutting_locations,colour in zip(enzyme_table_with_colour[1],enzyme_table_with_colour[3]):
        for location in cutting_locations:
            draw_enzyme(location*scale,colour,draw)
    del draw
    im.save("exons.png")