from PIL import Image, ImageDraw
import copy
from Object import Object
class Figure:

    def __init__(self, image_source):
        if isinstance(image_source, str):
            # Load image from file and make it black or white (no grey!)
            self.image = Image.open(image_source).convert('L').point(lambda x: 0 if x < 255 else 255, '1')
            #self.image = Image.open(image_source).convert('L').point(lambda x: 0 if x == 0 else 255, '1')
        elif isinstance(image_source, Image.Image):
            self.image = image_source.convert('L').point(lambda x: 0 if x < 255 else 255, '1')

        self.pixels = self.convert_image_to_pixels_array(self.image)
        self.objects = []

    def convert_image_to_pixels_array(self, image):
        pixels = list(image.getdata())
        width, height = image.size
        pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]

        return pixels

    # Identifies all contiguous figures in these images
    # Only includes black objects from the image
    # ((Assumes images are comprised of black and white pixels ONLY. no grey!))
    def identify_objects(self):
        im = copy.deepcopy(self.image)
        width, height = im.size

        dark_fill_val = 1
        light_fill_val = 254
        for x in range(width):
            for y in range(height):
                xy = (x, y)
                l_val = im.getpixel(xy)

                if l_val == 0:
                    ImageDraw.floodfill(im, xy, dark_fill_val)
                    self.objects.append(Object(xy, dark_fill_val))
                    dark_fill_val += 1
                elif l_val == 255:
                    ImageDraw.floodfill(im, xy, light_fill_val)
                    light_fill_val -= 1
                else:
                    for obj in self.objects:
                        if obj.l_val == l_val:
                            obj.add_pixel(xy)
                            break

    def find_centroids(self):
        for obj in self.objects:
            obj.find_centroid()
