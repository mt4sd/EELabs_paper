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

A=pd.read_csv(folder+'\Figura_9.csv')
bins2=(np.array(range(-20,20))/20)
ax.hist(A['Promedio'].values,bins2,histtype='stepfilled',color='gray',label='Average behavior (P50<21 mag)',linewidth=1.7,density=True, alpha=0.4)
ax.hist(A['stars2'].values,bins2,histtype='stepfilled',color='darkorange',linewidth=1.7,density=True, alpha=0.2)
ax.hist(A['stars2'].values,bins2,histtype='step',color='darkorange',label='stars2, good behavior',linewidth=1.7, alpha=0.8,density=True)
ax.hist(A['stars47'].values,bins2,histtype='stepfilled',color='green',linewidth=1.7,density=True, alpha=0.2)
ax.hist(A['stars47'].values,bins2,histtype='step',color='green',label='stars47, anomalous behavior',linewidth=1.7, alpha=0.8,density=True)

xlabel = r'm - P50 [mag/arcsec$^{2}$]'
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