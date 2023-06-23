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

A=pd.read_csv(folder+'\Figura_11.csv')

A=A[A['n']>2]

ax.scatter(A['n']*0.2,A['Izq_Der'],alpha=0.6,color='blue',marker='o',s=30,label='Interval growth of the regression from left to right')
ax.scatter(A['n']*0.2,A['Der_Izq'],alpha=0.6,color='red',marker='o',s=30,label='Interval growth of the regression from right to left')
ax.plot(A['n']*0.2,A['Izq_Der'],alpha=0.6,color='blue')
ax.plot(A['n']*0.2,A['Der_Izq'],alpha=0.6,color='red')
    


xlabel = r'Interval width [log(nW/(cm$^{2}$sr))]'
ylabel = r'RMSE [mag/arcsec$^{2}$]'


plt.xticks(A['n']*0.2)
ax.legend(fontsize=13)


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