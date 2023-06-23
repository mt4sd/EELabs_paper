import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import argparse

#Input of the script
parser = argparse.ArgumentParser()
parser.add_argument('--folder_data',  type=str,required=True,  help='Folder where the CSV files of the figures are located')
args = parser.parse_args()

folder = args.folder_data

A=pd.read_csv(folder+'\Figura_4.csv')

fig = plt.figure(1, figsize=(10,6))
plt.clf()
ax = plt.subplot(111)
xlabel = r'P50$_{ \mathrm{Without\ galaxy}}$ [mag/arcsec$^{2}$]'
ylabel = r'P50$_{ \mathrm{Without\ galaxy}}$ - P50$_{ \mathrm{With\ galaxy}}$ [mag/arcsec$^{2}$]'

ax.plot([15,24],[0,0],linestyle='--',linewidth=1.2,color='black',label='Todo hasta 21.5_r^2=0.80')
ax.errorbar(x=A['P50_sin_media'].values,y=A['Sin-con_media'].values,xerr=A['E_sin'],yerr=A['E_Sin-con'],capsize=1.5, fmt='none',barsabove=True,elinewidth=1,ecolor='black')

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

ax.set_ylim(-0.6,0.6)
ax.set_xlim(17.8,22)
 

plt.tight_layout()
plt.show()