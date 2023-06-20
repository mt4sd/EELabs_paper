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
ax = plt.subplot(121)
ax2=plt.subplot(122)

A=pd.read_csv(folder+'\Figura_8a.csv')
B=pd.read_csv(folder+'\Figura_8b.csv')

def Quitar_nulos(V):
    V=np.array(V)
    return V[~np.isnan(V)]

ax.boxplot([Quitar_nulos(A['19-18'].values),Quitar_nulos(A['20-19'].values),Quitar_nulos(A['21-20'].values),Quitar_nulos(A['22-21'].values)],labels=['18-19','19-20','20-21','21-22'],flierprops=dict(alpha=.8))
ax2.boxplot([Quitar_nulos(B['.1'].values),Quitar_nulos(B['.2'].values),Quitar_nulos(B['.3'].values)],labels=['0.00-0.13','0.13-0.27','0.27-0.40'],flierprops=dict(alpha=.8))

ylabel = r'A$_{BY}$'
xlabel = r'P50 [mag/arcsec$^{2}$]'
x2label = r'P75-P25 [mag/arcsec$^{2}$]'

fontsize=14
ax.set_xlabel(xlabel,fontsize=fontsize)
ax.set_ylabel(ylabel,fontsize=fontsize)

ax2.set_xlabel(x2label,fontsize=fontsize)

ax.minorticks_on()
ax.tick_params(axis='both',direction='in',which='minor',
               length=3,width=.5,labelsize=fontsize)
ax.tick_params(axis='both',direction='in',which='major',
               length=5,width=1,labelsize=fontsize)
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
    
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(1.2)

ax2.minorticks_on()
ax2.tick_params(axis='both',direction='in',which='minor',
               length=3,width=.5,labelsize=fontsize)
ax2.tick_params(axis='both',direction='in',which='major',
               length=5,width=1,labelsize=fontsize)
ax2.yaxis.set_ticks_position('both')
ax2.xaxis.set_ticks_position('both')
    
for axis in ['top','bottom','left','right']:
    ax2.spines[axis].set_linewidth(1.2)

ax.set_ylim(-.8,.7)
ax2.set_ylim(-.8,.7)

twin_axes=ax2.twiny()
twin_axes.minorticks_on()
twin_axes.tick_params(axis='both',direction='in',which='minor',
               length=3,width=.5,labelsize=fontsize)
twin_axes.tick_params(axis='both',direction='in',which='major',
               length=5,width=1,labelsize=fontsize)
twin_axes.boxplot([Quitar_nulos(B['.1'].values),Quitar_nulos(B['.2'].values),Quitar_nulos(B['.3'].values)],labels=['0.0-0.1','0.1-0.2','0.2-0.3'], boxprops=dict(alpha=0),flierprops=dict(alpha=0),whiskerprops=dict(alpha=0),capprops=dict(alpha=0))

twin_axes.set_xlabel(r'$\sigma_{1}$ [mag/arcsec$^{2}$]',fontsize=fontsize)

twin_axes.set_ylim(-.8,.7)


plt.tight_layout()
plt.show()