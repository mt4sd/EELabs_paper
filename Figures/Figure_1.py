import numpy as np
import matplotlib.pyplot as plt
import argparse

#Input of the script
parser = argparse.ArgumentParser()
parser.add_argument('--folder_data',  type=str,required=True,  help='Folder where the CSV files of the figures are located')
args = parser.parse_args()

folder = args.folder_data
folder=folder+'\Spectrum\ '

plt.rcParams["font.family"] = "serif"


def plotter(ax, x, y, xlabel, ylabel, color, label, fontsize=14,
            mk='.', lstyle='None', rast=False,aph=1,lw=1,mksz=1):

    ax.plot(x,y,color=color,label=label,marker=mk,linestyle=lstyle,
        rasterized=rast,alpha=aph,linewidth=lw,markersize=mksz)
     
    if label != None: ax.legend(loc=0,fontsize=fontsize-1,frameon=False)
    
    ax.set_xlabel(xlabel,fontsize=fontsize)
    ax.set_ylabel(ylabel,fontsize=fontsize)
    
    ax.minorticks_on()
    ax.tick_params(axis='both',direction='in',which='minor',
               length=3,width=.5,labelsize=fontsize)
    ax.tick_params(axis='both',direction='in',which='major',
               length=5,width=1,labelsize=fontsize)
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')
    
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(1.2)


fnames = ['Bessel_B.txt', 'Bessel_V.txt', 'Bessel_R.txt', 'Bessel_I.txt', 'T_SG_31_full.txt',
          'T_TESS_full.txt', 'T_SQM_full.txt','DNB_VIIRS.txt', 'Bskycalc.txt']
labels = [r'B', r'V', r'R', r'I', r'SG-WAS', r'TESS', r'SQM', r'VIIRS-DNB', r'Sky']
colors = ['blue', 'green', 'red', 'brown', 'brown', 'darkblue', 'goldenrod','darkgreen', 'k']

fig = plt.figure(1, figsize=(10,6))
plt.clf()
ax = plt.subplot(111)
xlabel = r'Wavelength $\lambda$ (nm)'
ylabel = r'Normalized responsivity'


for i in range(len(fnames)):
    l, r = np.loadtxt(folder[:-1]+fnames[i], unpack=True)

    if labels[i] == 'Sky':
        r = r[l< 1000]; l = l[l< 1000]
    
    if fnames[i][0] == 'B': # Solo normalizamos los filtros johnson
        r = r/r.max()
    lstyle = 'solid'


    if labels[i] == 'TESS': lw = 2.5
    elif labels[i] == 'SQM': lw = 2.5
    elif labels[i] == 'SG-WAS': lw = 2.5
    elif labels[i] == 'VIIRS-DNB': lw = 2.5
    else: lw = 0.9

    if i < 4: lstyle = 'dashed'
    if i == 7: lstyle = 'dashdot'

    plotter(ax, l, r, xlabel, ylabel, colors[i],
            labels[i], mk=None, lstyle=lstyle,lw=lw)
    
ax.set_xlim(220,1000)
ax.set_ylim(-0.03,1.03)

ax.text(530,0.55,r'[OI]'+'\n'+'557.7',fontsize=12,multialignment='center')
ax.text(630.7,0.38,r'[OI]'+'\n'+'630.0',fontsize=12,multialignment='center')
ax.text(572,0.13,r'Na D'+'\n'+'589.0'+'\n'+'589.6',fontsize=12,multialignment='center')
ax.text(647,0.77,'________________________________________________________',fontsize=10,multialignment='center')
ax.text(850,0.78,'OH bands',fontsize=12,multialignment='center')

plt.tight_layout()
plt.show()
plt.savefig('spectra.pdf', dpi=1000)