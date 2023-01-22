

#
# Vaious examples of the usage of the smith modules
# These examples aare used to generate diffeerent figures of the Radio Engineering 1 design exercise.
#

import sys
sys.path.append('/home/aissa/Downloads/test/py-microwave/modules')

import subprocess

import matplotlib.pyplot as plt
from numpy import *
from smith import *

def get_gamma(Z):
    return (Z-50)/(Z+50)

def get_Z(gamma): 
    return 50*(1+gamma)/(1-gamma)



f = 2e9
w = 2*pi*f
S_opt = -0.0666 + 0.4390j
# S_opt = 1j
Lin = 3.1691e-09
Cin = 2.7909e-12

# gamma_out = S22 + (gamma_S*S21*S12)/(1-gamma_S*S11)
gamma_out = 0.3962 - 0.5248j
L_stab = 10e-9 ;
R_stab = 30 ;
Z_stability = R_stab + 1j*w*L_stab
Lout = 6.9719e-09
Cout = 1.1551e-12


# demo = 'input'
demo = 'output'

if demo == 'input':

    ## Plot smithchart
    fig, ax = plt.subplots(figsize=(10, 10))
    # fig, ax = plt.subplots()
    Z0 = 50
    mysmith = Smith(ax, 'both', Z0, fineness=1)
    # mysmith = Smith(ax, 'none', Z0)
    # mysmith.addpolargrid()
    # mysmith.addanglering()

    Z1 = mysmith.addstart( get_Z( conj(S_opt) ) )
    Z2 = mysmith.addpara(Z1, 1j*w*Lin )
    Z3 = mysmith.addseries(Z2, 1/(1j*w*Cin) )

    # mysmith.addangle(Z2)
    # mysmith.addangle(Z3)

    mysmith.addpoint(Z1, '$Z^{*}_{opt}$', 'S' )
    mysmith.addpoint(Z2, '$Z_{in, with \ Lin}$', 'NE')
    mysmith.addpoint(Z3, '$Z_{in, with \ Cin}$', 'W')
    # file = superimposeChart(fig)

    ## for hand analysis & debugging
    # for ele in mysmith.circuit:
    #     Z = ele.Zin
    #     n = ele.id
    #     Gam = my_magphase_tex((Z - Z0) / (Z + Z0))
    #     print('$Z_{0:1} = ({1:4.2f}) \;\Omega \qquad \Gamma_{0:1} = {2:s}$ \n'.format(n, Z, Gam))

    Zin = Z3
    gam = get_gamma(Zin)

    # Input_smithChart_paper = superimposeChart(fig,'Input_smithChart_paper.svg')

    fig.savefig("Input_smithChart.pdf",transparent=True)
    bashCommand = "pdfcrop Input_smithChart.pdf"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    # output, error = process.communicate()

    plt.show()
    plt.close(fig)

    ## Create a circuit schematic of the analysed circuit  ##

    d = mysmith.plotschematic()
    d.draw()  # must be set to false, otherwise plot will draw already in schemdraw module
    plt.tight_layout()
    d.save("Input_schematic.pdf")
    # plt.show()



if demo == 'output':

    ## Plot smithchart
    fig, ax = plt.subplots(figsize=(10, 10))
    Z0 = 50
    mysmith = Smith(ax, 'both', Z0, fineness=1)
    # mysmith.addpolargrid()
    # mysmith.addanglering()

    Z1 = mysmith.addstart( get_Z( gamma_out ) )
    Z2 = mysmith.addpara(Z1, Z_stability )
    Z3 = mysmith.addpara(Z2, 1j*w*Lout )
    Z4 = mysmith.addseries(Z3, 1/(1j*w*Cout) )


    mysmith.addpoint(Z1, '$Z_{out}$', 'S' )
    mysmith.addpoint(Z2, '$Z_{out, with \ Stab \ Ckt}$', 'NE')
    mysmith.addpoint(Z3, '$Z_{out, with \ Lout}$', 'NW')
    mysmith.addpoint(Z4, '$Z_{out, with \ Cout}$', 'W')
    # file = superimposeChart(fig)

    Zin = Z4
    gam = get_gamma(Zin)

    fig.savefig("Output_smithChart.pdf",transparent=True)
    bashCommand = "pdfcrop Output_smithChart.pdf"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    # output, error = process.communicate()

    plt.show()
    plt.close(fig)

    ## Create a circuit schematic of the analysed circuit  ##

    d = mysmith.plotschematic()
    d.draw()  # must be set to false, otherwise plot will draw already in schemdraw module
    plt.tight_layout()
    d.save("Output_schematic.pdf")
