from PIL import Image, ImageFilter, ImageOps


# Edge finding
#image1 = Image.open('1.png')
image7 = Image.open('7.png')
image8 = Image.open('8.png')
images = [image8, image7]

for image in images:
    image = image.filter(ImageFilter.CONTOUR).convert('L').point(lambda x: 0 if x < 128 else 255, '1')
    image.show()

    '''
    image = image.filter(ImageFilter.FIND_EDGES)
    image.show()
    image = image.convert('L').point(lambda x: 0 if x < 255 else 255, '1')
    image.show()
    ImageOps.invert(image)
    image.show()
'''
pass

'''
filename = "Lenna.png"
original = Image.open("Lenna.png")
im = original.crop((0, 0, 100, 100))
im.show()
pass
try:
    original = Image.open("Lenna.png")
    original2 = Image.open("Lenna.png")
    mod = Image.open("Lenna2.png")
    duplicate = Image.open("LennaDup.png")


    im = original.crop(0, 0, 100, 100)
    im.show()

    # Does pixel by pixel comparison to determine equality
    if original == original2:
        print "they're equal same"
    if original == mod:
        print "they're equal mod"
    if original == duplicate:
        print "they're equal dup"

    print "The size of the Image is: "
    print(original.format, original.size, original.mode)

except:
    print "unable to load image"
'''

'''
ImageOps
    mirror  (horizontal)
    flip    (vertical)
    invert  (negates image)
    fit     (???)

ImageChops
    add
    add_modulo
    composite   (???)
    difference  (pixel-by-pixel difference)
    logical_and
    logical_or
    offset
    subtract
    subtract_modulo

'''