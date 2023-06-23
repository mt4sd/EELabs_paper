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

A=pd.read_csv(folder+'\Figura_12.csv')

T=['_all','_TESS','_SG']
color=['darkgreen','darkblue','darkred']
m=[-0.9497474472911072,-0.9567199735874145,-0.8913937954850185]
n=[20.929127435594243,20.93330572908256,20.93545127290887]
marca=['o','v','s']
texto=['All photometers=20.93$\pm$ 0.07$-$(0.95 $\pm$ 0.10) x log(VIIRS) , r$^{2}=0.96$','TESS=20.93 $\pm$ 0.07$-$(0.96 $\pm$ 0.11) x log(VIIRS), r$^{2}=0.96$','SG=20.94 $\pm$ 0.24$-$(0.89 $\pm$ 0.24) x log(VIIRS), r$^{2}=0.82$']
for i in range(0,3):
    text=T[i]
    B=A
    ax.errorbar(x=B['DNB_BRDF_Corrected_NTL_log_P50'+text].values,y=B['P50_fot'+text].values,xerr=B['E_sat_t'+text],yerr=B['E_fot_t'+text],capsize=1.5, fmt='none',barsabove=True,elinewidth=1,ecolor=color[i])
    ax.scatter(B['DNB_BRDF_Corrected_NTL_log_P50'+text].values,B['P50_fot'+text].values,alpha=0.6,color=color[i],marker=marca[i],s=30,label=texto[i])#)
    ax.plot(np.linspace(-2,3),m[i]*np.linspace(-2,3)+n[i],linestyle='-',linewidth=1,color=color[i])

ax.axvline(1.6, color="black",linewidth=1,linestyle='--',alpha=1)
ax.axvline(-0.2, color="black",linewidth=1,linestyle='--',alpha=1)
ax.fill([1.6,-0.2,-0.2,1.6],[22,22,17.3,17.3],color='gray',alpha=.2)

plt.text(-0.2+(1.6+.3)/2,19.2, 'Regression interval',fontsize=15,color='black', horizontalalignment='center',verticalalignment='center')
plt.text(-0.2+0.1,21.8, '-0.2',fontsize=12,color='black', horizontalalignment='center',verticalalignment='center')
plt.text(1.6+0.1,21.8, '1.6',fontsize=12,color='black', horizontalalignment='center',verticalalignment='center')

xlabel = r'P50$_{\mathrm{log (VIIRS)}}$ [log(nW/(cm$^{2}$sr))]'
ylabel = r'P50$_{ \mathrm{photometers}}$ [mag/arcsec$^{2}$]'

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

ax.set_xlim(-1.6,2.5)
ax.set_ylim(17.3,22)
ax.invert_yaxis()

plt.tight_layout()
plt.show()