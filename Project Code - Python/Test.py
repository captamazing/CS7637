from Figure import Figure
from Object import Object

fig1 = Figure("1.png")
fig7 = Figure("7.png")
fig8 = Figure("8.png")

fig_a = Figure("Problems/Basic Problems D/Basic Problem D-02/A.png")
fig_b = Figure("Problems/Basic Problems D/Basic Problem D-02/B.png")
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

