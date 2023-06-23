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
ax = plt.subplot(111)

A=pd.read_csv(folder+'\Figura_13.csv')
bins=(np.array(range(190,220))/10)
ax.hist(A['LPL15_030'].values,bins,histtype='stepfilled',color='brown',linewidth=1.7,density=True, alpha=0.2)
ax.hist(A['LPL15_030'].values,bins,histtype='step',color='brown',label='LPL15_030, P50=20.93 mag/arcsec$^{2}$',linewidth=1.7,density=True)
ax.hist(A['LPL15_045'].values,bins,histtype='stepfilled',color='darkorange',linewidth=1.7,density=True, alpha=0.2)
ax.hist(A['LPL15_045'].values,bins,histtype='step',color='darkorange',label='LPL15_045, P50=20.50 mag/arcsec$^{2}$',linewidth=1.7,density=True)
ax.hist(A['stars767'].values,bins,histtype='stepfilled',color='green',linewidth=1.7,density=True, alpha=0.2)
ax.hist(A['stars767'].values,bins,histtype='step',color='green',label='stars767, P50=20.70 mag/arcsec$^{2}$',linewidth=1.7,density=True)
ax.hist(A['stars770'].values,bins,histtype='stepfilled',color='blue',linewidth=1.7,density=True, alpha=0.2)
ax.hist(A['stars770'].values,bins,histtype='step',color='blue',label='stars770, P50=20.63 mag/arcsec$^{2}$',linewidth=1.7,density=True)
ax.hist(A['sat'].values,bins,histtype='stepfilled',color='gray',linewidth=1.7,density=True, alpha=0.4)
ax.hist(A['sat'].values,bins,histtype='step',color='gray',label='VIIRS, P50=20.61 mag/arcsec$^{2}$',linewidth=1.7,density=True,linestyle='--')

xlabel = r'm [mag/arcsec$^{2}$]'
ylabel = r'Density'

ax.legend(loc='upper left',fontsize=13)

fontsize=14
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

plt.tight_layout()
plt.show()