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

A=pd.read_csv(folder+'\Figura_7.csv')

def Quitar_nulos(V):
    V=np.array(V)
    return V[~np.isnan(V)]

ax.boxplot([Quitar_nulos(A['19-18'].values),Quitar_nulos(A['20-19'].values),Quitar_nulos(A['21-20'].values),Quitar_nulos(A['22-21'].values)],labels=['18-19','19-20','20-21','21-22'],flierprops=dict(alpha=.8))

ylabel = r'P75-P25 [mag/arcsec$^{2}$]'
xlabel = r'P50 [mag/arcsec$^{2}$]'

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

ax.set_ylim(-0.1,1)

twin_axes=ax.twinx() 
twin_axes.minorticks_on()
twin_axes.tick_params(axis='both',direction='in',which='minor',
               length=3,width=.5,labelsize=fontsize)
twin_axes.tick_params(axis='both',direction='in',which='major',
               length=5,width=1,labelsize=fontsize)
twin_axes.boxplot([Quitar_nulos(A['19-18'].values)/(0.67*2),Quitar_nulos(A['20-19'].values)/(0.67*2),Quitar_nulos(A['21-20'].values)/(0.67*2),Quitar_nulos(A['22-21'].values)/(0.67*2)],labels=['18-19','19-20','20-21','21-22'], boxprops=dict(alpha=0),flierprops=dict(alpha=0),whiskerprops=dict(alpha=0),capprops=dict(alpha=0))

twin_axes.set_ylabel(r'$\sigma_{1}$ [mag/arcsec$^{2}$]',fontsize=fontsize)

twin_axes.set_ylim(-0.1/(0.67*2),1/(0.67*2))

plt.tight_layout()
plt.show()