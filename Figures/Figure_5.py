import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import argparse

#Input of the script
parser = argparse.ArgumentParser()
parser.add_argument('--folder_data',  type=str,required=True,  help='Folder where the CSV files of the figures are located')
args = parser.parse_args()

folder = args.folder_data


fig, axes = plt.subplots(nrows=1, ncols=2,figsize=(10,6))

ax=axes[0]
ax2=axes[1]


A=pd.read_csv(folder+'\Figura_5a.csv')
bins2=(np.array(range(-20,20))/20)

def Gauss(x,sigma):
    return np.exp(-x**2/(2*sigma**2))/(np.sqrt(2*np.pi)*sigma)



X=np.linspace(bins2[0],bins2[-1],100)

ax.plot(X,[Gauss(i,0.1) for i in X],linestyle=(0,(3,6)),color='black',linewidth=1.4,alpha=0.7)
ax.plot(X,[Gauss(i,0.2) for i in X],linestyle=(0,(3,6)),color='black',linewidth=1.4,alpha=0.6)
ax.plot(X,[Gauss(i,0.3) for i in X],linestyle=(0,(3,6)),color='black',linewidth=1.4,alpha=0.5)


ax.hist(A['Con_outliers_>21'].values,bins2,histtype='step',color='darkorange',label='Average behavior P50>21 mag/arcsec$^{2}$',linewidth=1.7, alpha=1,density=True)
ax.hist(A['Con_outliers_<21'].values,bins2,histtype='step',color='green',label='Average behavior P50<21 mag/arcsec$^{2}$',linewidth=1.7, alpha=1,density=True)




xlabel = r'm - P50 [mag/arcsec$^{2}$]'
xlabel2 = r'N(0,0.1) quantiles [mag/arcsec$^{2}$]'
ylabel = r'Density'
ylabel2 = r'Data normalized quantiles [mag/arcsec$^{2}$]'


ax.legend(loc='upper left',fontsize=11)

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

ax.set_ylim(0,4.8)

ax.text(-0.38,3,'$\sigma$=0.1',fontsize=12,multialignment='center')
ax.text(-0.42,1.8,'$\sigma$=0.2',fontsize=12,multialignment='center')
ax.text(-0.52,1,'$\sigma$=0.3',fontsize=12,multialignment='center')

ax.set_xlabel(xlabel,fontsize=fontsize)
ax.set_ylabel(ylabel,fontsize=fontsize)

AA=pd.read_csv(folder+'\Figura_5b.csv')

x=AA['Gauss_01'].values
ax2.plot(x,AA['Gauss_01'].values,linewidth=1,color='black',linestyle='--',alpha=.8)
ax2.plot(x,AA['Gauss_02'].values,linewidth=1,color='black',linestyle='--',alpha=.8)
ax2.plot(x,AA['Gauss_03'].values,linewidth=1,color='black',linestyle='--',alpha=.8)


ax2.plot(x,AA['Con_outliers_>21'].values,linewidth=1.7,color='darkorange',label='Average behavior P50>21',alpha=1)
ax2.plot(x,AA['Con_outliers_<21'].values,linewidth=1.7,color='green',label='Average behavior P50<21',alpha=1)

ax2.axvline(x=0.067, color="black",linewidth=0.8,linestyle='-.',alpha=1)
ax2.axvline(x=0, color="black",linewidth=0.8,linestyle='-.',alpha=1)
ax2.axvline(x=-0.067, color="black",linewidth=0.8,linestyle='-.',alpha=1)

ax2.minorticks_on()
ax2.tick_params(axis='both',direction='in',which='minor',
               length=3,width=.5,labelsize=fontsize)
ax2.tick_params(axis='both',direction='in',which='major',
               length=5,width=1,labelsize=fontsize)
ax2.yaxis.set_ticks_position('both')
ax2.xaxis.set_ticks_position('both')
    
for axis in ['top','bottom','left','right']:
    ax2.spines[axis].set_linewidth(1.2)

ax2.set_ylim(-1,1)
ax2.set_xlim(x[0]-.07,x[-1])

ax2.text(0.067+.003,-0.75,'P75',fontsize=fontsize-1,multialignment='center')
ax2.text(0+.003,-0.75,'P50',fontsize=fontsize-1,multialignment='center')
ax2.text(-0.067+.003,-0.75,'P25',fontsize=fontsize-1,multialignment='center')

ax2.text(-0.29,-0.2,'$\sigma$=0.1',fontsize=10,multialignment='center')
ax2.text(-0.29,-0.44,'$\sigma$=0.2',fontsize=10,multialignment='center')
ax2.text(-0.29,-0.66,'$\sigma$=0.3',fontsize=10,multialignment='center')

ax2.set_xlabel(xlabel2,fontsize=fontsize)
ax2.set_ylabel(ylabel2,fontsize=fontsize)

plt.tight_layout()
plt.show()