from PIL import Image, ImageDraw

height=50
centre = height/2
def draw_intron(start,length,draw):
    draw.rectangle([start,centre-3,start+length,centre+3],fill='red',outline='black')

def draw_exon(start,end,draw):
    draw.rectangle([start,centre-10,end,centre+10],fill='green',outline='black')

def draw_gene(DNA,CDS_loc):
    im = Image.new("RGB", (len(DNA), height), "white")
    draw = ImageDraw.Draw(im)
    draw_intron(0,len(DNA),draw)
    for i in CDS_loc:
        draw_exon(i[0],i[1]+1,draw)
    del draw
    im.save("TEST.bmp")