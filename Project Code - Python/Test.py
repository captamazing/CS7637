from Figure import Figure
from PIL import Image
from Object import Object
import copy

def figure_and(fig1, fig2):
    im1 = fig1.image
    im2 = fig2.image
    if im1.size != im2.size:
        raise Exception('Images must be same size to AND them')
    size = im1.size
    image = Image.new('L', size, color=255)

    for x in range(size[0]):
        for y in range(size[1]):
            xy = x, y
            if im1.getpixel(xy) == im2.getpixel(xy) == 0:
                image.putpixel(xy, 0)
    return Figure(image)

def figure_xor(fig1, fig2):
    im1 = fig1.image
    im2 = fig2.image
    if im1.size != im2.size:
        raise Exception('Images must be same size to XOR them')
    size = im1.size
    image = Image.new('L', size, color=255)

    for x in range(size[0]):
        for y in range(size[1]):
            xy = x, y
            if im1.getpixel(xy) != im2.getpixel(xy):
                image.putpixel(xy, 0)
    return Figure(image)

def figure_add(fig1, fig2):
    if fig1.image.size != fig2.image.size:
        raise Exception('Figures must be same size to SUBTRACT them')

    size = fig1.image.size
    image = Image.new('L', size, color=255)

    for obj1 in fig1.objects:
        for xy in obj1.area:
            image.putpixel(xy, 0)

    for obj2 in fig2.objects:
        for xy in obj2.area:
            image.putpixel(xy, 0)

    return Figure(image)

def figure_subtract(fig1, fig2):
    if fig1.image.size != fig2.image.size:
        raise Exception('Figures must be same size to SUBTRACT them')

    image = copy.deepcopy(fig1.image)

    for obj2 in fig2.objects:
        for xy in obj2.area:
            image.putpixel(xy, 255)

    return Figure(image)

fig_e10_a = Figure("E-10-A.png")
fig_e10_b = Figure("E-10-B.png")

print 'Identifying objects...'
fig_e10_a.identify_objects()
fig_e10_b.identify_objects()

print 'Doing the maths...'
figure_and(fig_e10_a, fig_e10_b)
figure_xor(fig_e10_a, fig_e10_b)
figure_add(fig_e10_b, fig_e10_a)
figure_subtract(fig_e10_b, fig_e10_a)

print 'Done\n'


'''
fig1 = Figure("1.png")
fig7 = Figure("7.png")
fig8 = Figure("8.png")

fig_a = Figure("Problems/Basic Problems D/Basic Problem D-02/E-10-A.png")
fig_b = Figure("Problems/Basic Problems D/Basic Problem D-02/E-10-B.png")
fig_c = Figure("Problems/Basic Problems D/Basic Problem D-02/C.png")
fig_d = Figure("Problems/Basic Problems D/Basic Problem D-02/D.png")
fig_e = Figure("Problems/Basic Problems D/Basic Problem D-02/E.png")
fig_f = Figure("Problems/Basic Problems D/Basic Problem D-02/F.png")
fig_g = Figure("Problems/Basic Problems D/Basic Problem D-02/G.png")
fig_h = Figure("Problems/Basic Problems D/Basic Problem D-02/H.png")


figs = [fig_a, fig_b, fig_c,
        fig_d, fig_e, fig_f,
        fig_g, fig_h]

for fig in figs:
    fig.identify_objects()


if fig_a.objects[0] == fig_e.objects[0]:
    print 'A and E are equal'

if fig_a.objects[0] == fig_b.objects[0]:
    print 'A and B are equal'
'''


