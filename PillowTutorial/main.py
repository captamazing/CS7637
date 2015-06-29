from PIL import Image, ImageFilter

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