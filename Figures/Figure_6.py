import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Rectangle
import argparse

#Input of the script
parser = argparse.ArgumentParser()
parser.add_argument('--folder_data',  type=str,required=True,  help='Folder where the CSV files of the figures are located')
args = parser.parse_args()

folder = args.folder_data

fig = plt.figure(1, figsize=(10,6))
plt.clf()
ax = plt.subplot(2,2,1)

A=pd.read_csv(folder+'\Figura_6.csv')

ax.scatter(A['P50'].values,A['P75-P25'].values,alpha=0.6)
ax.axhline(y=0.1*(0.67*2), color="black",linewidth=0.8,linestyle='-.',alpha=1)
#ax.axhline(y=0.15*(0.67*2), color="black",linewidth=0.8,linestyle='-.',alpha=1)
ax.axhline(y=0.4, color="red",linewidth=0.8,linestyle='-',alpha=1)

#plt.rcParams["font.family"] = "serif"


xlabel = r'P50 [mag/arcsec$^{2}$]'
ylabel = r'P75-P25 [mag/arcsec$^{2}$]'



#ax.legend(fontsize=13)


fontsize=14
#ax.set_xlabel(xlabel,fontsize=fontsize)
#ax.set_ylabel(ylabel,fontsize=fontsize)


ax.minorticks_on()
ax.tick_params(axis='both',direction='in',which='minor',
               length=3,width=.5,labelsize=fontsize)
ax.tick_params(axis='both',direction='in',which='major',
               length=5,width=1,labelsize=fontsize)
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')

ax.set_xlim(17,22.5)

twin_axes=ax.twinx() 
twin_axes.minorticks_on()
twin_axes.tick_params(axis='both',direction='in',which='minor',
               length=3,width=.5,labelsize=fontsize)
twin_axes.tick_params(axis='both',direction='in',which='major',
               length=5,width=1,labelsize=fontsize)
twin_axes.scatter(A['P50'].values,A['P75-P25'].values/(0.67*2),alpha=0)
twin_axes.set_ylabel(r'$\sigma_{1}$ [mag/arcsec$^{2}$]',fontsize=fontsize)
    
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(1.2)

ax2 = plt.subplot(2,2,3)
ax2.scatter(A['P50'].values,A['P75-P25'].values,alpha=0.6)
ax2.axhline(y=0.1*(0.67*2), color="black",linewidth=0.8,linestyle='-.',alpha=1)
#ax2.axhline(y=0.15*(0.67*2), color="black",linewidth=0.8,linestyle='-.',alpha=1)
ax2.axhline(y=0.4, color="red",linewidth=0.8,linestyle='-',alpha=1)

x1, x2, y1, y2 = 18, 22, 0, 0.4*(0.67*2)
ax2.set_xlim(x1, x2)
ax2.set_ylim(y1, y2)

ax2.minorticks_on()
ax2.tick_params(axis='both',direction='in',which='minor',
               length=3,width=.5,labelsize=fontsize)
ax2.tick_params(axis='both',direction='in',which='major',
               length=5,width=1,labelsize=fontsize)
ax2.yaxis.set_ticks_position('both')
ax2.xaxis.set_ticks_position('both')

for axis in ['top','bottom','left','right']:
    ax2.spines[axis].set_linewidth(1.2)

twin_axes2=ax2.twinx() 
twin_axes2.minorticks_on()
twin_axes2.tick_params(axis='both',direction='in',which='minor',
               length=3,width=.5,labelsize=fontsize)
twin_axes2.tick_params(axis='both',direction='in',which='major',
               length=5,width=1,labelsize=fontsize)
twin_axes2.scatter(A['P50'].values,A['P75-P25'].values/(0.67*2),alpha=0)
twin_axes2.set_ylabel(r'$\sigma_{1}$ [mag/arcsec$^{2}$]',fontsize=fontsize)
twin_axes2.set_ylim(y1/(0.67*2), y2/(0.67*2))

ax3 = plt.subplot(2,2,4)
ax3.scatter(A['P50'].values,A['STD'].values,alpha=0.6)
ax3.axhline(y=0.1, color="black",linewidth=0.8,linestyle='-.',alpha=1)
#ax3.axhline(y=0.15, color="black",linewidth=0.8,linestyle='-.',alpha=1)
x1, x2, y1, y2 = 18, 22, 0, 0.4
ax3.set_xlim(x1, x2)
ax3.set_ylim(y1, y2)

ax3.yaxis.tick_right()

ax3.minorticks_on()
ax3.tick_params(axis='both',direction='in',which='minor',
               length=3,width=.5,labelsize=fontsize)
ax3.tick_params(axis='both',direction='in',which='major',
               length=5,width=1,labelsize=fontsize)
ax3.yaxis.set_ticks_position('both')
ax3.xaxis.set_ticks_position('both')

for axis in ['top','bottom','left','right']:
    ax3.spines[axis].set_linewidth(1.2)

ax3.yaxis.set_label_position('right')
ax3.set_ylabel(r'$\sigma_{2}$ [mag/arcsec$^{2}$]',fontsize=fontsize)

ax4 = plt.subplot(2,2,2)

ax4.scatter(A['P50'].values,A['STD'].values,alpha=0.6)
ax4.axhline(y=0.1*(0.67*2), color="black",linewidth=0.8,linestyle='-.',alpha=1)
#ax4.axhline(y=0.15*(0.67*2), color="black",linewidth=0.8,linestyle='-.',alpha=1)

ax4.yaxis.tick_right()

ax4.minorticks_on()
ax4.tick_params(axis='both',direction='in',which='minor',
               length=3,width=.5,labelsize=fontsize)
ax4.tick_params(axis='both',direction='in',which='major',
               length=5,width=1,labelsize=fontsize)
ax4.yaxis.set_ticks_position('both')
ax4.xaxis.set_ticks_position('both')

ax4.set_xlim(17,22.5)


    
for axis in ['top','bottom','left','right']:
    ax4.spines[axis].set_linewidth(1.2)

ax4.yaxis.set_label_position('right')
ax4.set_ylabel(r'$\sigma_{2}$ [mag/arcsec$^{2}$]',fontsize=fontsize)

fig.supxlabel(xlabel,fontsize=fontsize)
fig.supylabel(ylabel,fontsize=fontsize)

roi=[18,22,0,0.4*(0.67*2)]
ax.add_patch(Rectangle([roi[0],roi[2]], roi[1]-roi[0], roi[3]-roi[2],**dict([('fill',False), ('linestyle','-'), ('color','black'), ('linewidth',1)]) ))
ax4.add_patch(Rectangle([roi[0],roi[2]], roi[1]-roi[0], roi[3]-roi[2],**dict([('fill',False), ('linestyle','-'), ('color','black'), ('linewidth',1)]) ))

ax.text(22.1,4.1,'A)',fontsize=fontsize-1,multialignment='center')
ax4.text(22.1,2.1,'B)',fontsize=fontsize-1,multialignment='center')
ax2.text(21.7,0.47,'C)',fontsize=fontsize-1,multialignment='center')
ax3.text(21.7,0.35,'D)',fontsize=fontsize-1,multialignment='center')
ax.text(21.7,.7,'C)',fontsize=fontsize-1,multialignment='center')
ax4.text(21.7,.6,'D)',fontsize=fontsize-1,multialignment='center')


plt.tight_layout()
plt.show()