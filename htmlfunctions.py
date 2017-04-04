from PIL import Image, ImageDraw

'''Parameters for exon diagram'''
height=50
width = 1000
v_midpoint = height/2
exon_height = 10
intron_height = 10
enzyme_marker_height = 15

'''Draw a rectangle to represent an intron'''
def draw_intron(start,end,draw):
    x0 = start
    y0 = v_midpoint-intron_height/2
    x1 = end
    y1 = v_midpoint + intron_height/2
    draw.rectangle([x0,y0,x1,y1],fill='red',outline='black')

'''Draw a rectangle to represent the introns'''
def draw_exon(start,end,draw):
    x0 = start
    y0 = v_midpoint-exon_height/2
    x1 = end
    y1 = v_midpoint + exon_height/2
    draw.rectangle([x0,y0,x1,y1],fill='green',outline='black')

'''Draw an ellipse to represent the cutting point of an enzyme'''
def draw_enzyme(location,width,colour,draw):
    x0 = location - width/4
    y0 = v_midpoint - width
    x1 = location + width/4
    y1 = v_midpoint + width
    draw.ellipse([x0,y0,x1,y1],fill=colour,outline = 'black')


'''Draw a diagram of a gene showing exons and enzyme cutting locations and save it to "exons.png"'''
def draw_gene(DNA,CDS_loc,enzyme_table):
    im = Image.new("RGB", (width, height), "white") # len(DNA) and height are the dimensions of the image, CHANGED WIDTH TO 500
    scale = width/len(DNA)
    draw = ImageDraw.Draw(im)
    draw_intron(0,len(DNA)*scale,draw)
    for i in CDS_loc:
        draw_exon(i[0]*scale,(i[1]+1)*scale,draw)
    for cutting_locations,colour in zip(enzyme_table[1],enzyme_table[3]):
        for location in cutting_locations:
            draw_enzyme(location*scale,enzyme_marker_height,colour,draw)
    del draw
    im.save("exons.png")


"""Highlight the coding region of the DNA sequence"""
def highlightCDS(DNA,CDS_loc):
    opening_tag = '<mark>'
    closing_tag = '</mark>'
    j = 0
    tagged_DNA = ''
    for i in CDS_loc:
        tagged_DNA += DNA[j:i[0]] + opening_tag + DNA[i[0]:i[1] + 1] + closing_tag
        j = i[1] + 1
    tagged_DNA += DNA[j:]
    return tagged_DNA