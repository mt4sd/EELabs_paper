import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import argparse

#Input of the script
parser = argparse.ArgumentParser()
parser.add_argument('--folder_data',  type=str,required=True,  help='Folder where the CSV files of the figures are located')
args = parser.parse_args()

folder = args.folder_data

fig = plt.figure(1, figsize=(10,6))
plt.clf()
ax = plt.subplot(211)
ax2 = plt.subplot(212)

A=pd.read_csv(folder+'\Figura_2a.csv')
bins=(np.array(range(0,51))/10-1)[::2]
ax.hist(A['TESS'].values,bins,histtype='step',color='darkblue',label='TESS photometers',linewidth=1.7)
ax.hist(A['TESS'].values,bins,histtype='stepfilled',color='darkblue',linewidth=1.7, alpha=0.2)
ax.hist(A['SG'].values,bins,histtype='step',color='darkred',label='SG photometers',linewidth=1.7)
ax.hist(A['SG'].values,bins,histtype='stepfilled',color='darkred',linewidth=1.7, alpha=0.2)

xlabel = r'P50$_{\mathrm{log (VIIRS)}}$ [log(nW/(cm$^{2}$sr))]'
ylabel = r'Quantity of photometers'



ax.legend(fontsize=13)

fontsize=14



ax.minorticks_on()
ax.tick_params(axis='both',direction='in',which='minor',
               length=3,width=.5,labelsize=fontsize)
ax.tick_params(axis='both',direction='in',which='major',
               length=5,width=1,labelsize=fontsize)
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
    
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(1.2)

ax.set_xlim(-1.1,2.5)

AA=pd.read_csv(folder+'\Figura_2b.csv')
bins=(np.array(range(0,51))/10-1)[::2]
ax2.hist(AA['TESS'].values,bins,histtype='step',color='darkblue',label='TESS photometers',linewidth=1.7)
ax2.hist(AA['TESS'].values,bins,histtype='stepfilled',color='darkblue',linewidth=1.7, alpha=0.2)
ax2.hist(AA['SG'].values,bins,histtype='step',color='darkred',label='SG photometers',linewidth=1.7)
ax2.hist(AA['SG'].values,bins,histtype='stepfilled',color='darkred',linewidth=1.7, alpha=0.2)

ax2.minorticks_on()
ax2.tick_params(axis='both',direction='in',which='minor',
               length=3,width=.5,labelsize=fontsize)
ax2.tick_params(axis='both',direction='in',which='major',
               length=5,width=1,labelsize=fontsize)
ax2.yaxis.set_ticks_position('both')
ax2.xaxis.set_ticks_position('both')
    
for axis in ['top','bottom','left','right']:
    ax2.spines[axis].set_linewidth(1.2)

ax2.set_xlim(-1.1,2.5)

fig.supxlabel(xlabel,fontsize=fontsize)
fig.supylabel(ylabel,fontsize=fontsize)

plt.tight_layout()
plt.show()