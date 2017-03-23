from PIL import Image, ImageDraw

im = Image.new("RGB", (512, 512), "white")
draw = ImageDraw.Draw(im)
draw.rectangle([0,0,100,100],fill=(200,200,200))
draw.polygon()
del draw
im.save("TEST.bmp")