import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.colors as mcolors
import argparse

#Input of the script
parser = argparse.ArgumentParser()
parser.add_argument('--folder_data',  type=str,required=True,  help='Folder where the CSV files of the figures are located')
args = parser.parse_args()

folder = args.folder_data


Fotometros_N=['stars495','stars202','stars1','stars550','LPL1_050','LPL2_104','LPL3_104','LPL3_110']

fig, axes = plt.subplots(nrows=1, ncols=2,figsize=(10,6))


# Function to smooth the sawtooth teeth
def Smooth(n,v):
    v=list(v)
    lenght=len(v)
    V=[v[0]]*n+v+[v[-1]]*n
    W=0
    for i in range(0,n*2+1):
        W=W+np.array(V[0+i:lenght+i])
    return W/(n*2+1)

ax=axes[0]
ax2=axes[1]

fontsize=14
xlabel = r'Sample size'
xlabel2 = r'Sample size'
ylabel = r'$\Delta$ (P75-P25) [mag/arcsec$^{2}$]'
ylabel2 = r'$\Delta$ P50 [mag/arcsec$^{2}$]'


A=pd.read_csv(folder+'\Figura_3a.csv')

x=np.arange(100, 3000, 10)
colores=['darkred','darkorange','green','darkblue']
list(mcolors.TABLEAU_COLORS)
for i in range(0,len(Fotometros_N)):
    if i<4:
        ax.plot(x,Smooth(30,A[Fotometros_N[i]].values/2),linewidth=1.5,color=colores[i],alpha=.9,label=Fotometros_N[i])
    else:
        ax.plot(x[:100],Smooth(30,A[Fotometros_N[i]].values[:100]/2),linewidth=1.5,color=colores[i-4],linestyle='--',alpha=.9,label=Fotometros_N[i])
ax.axvline(x=500, color="red",linewidth=1.2,linestyle='-',alpha=1)
ax.text(380,0.0018,'500',fontsize=12,multialignment='center')

#ax.legend(loc='upper right',fontsize=11)

ax.minorticks_on()
ax.tick_params(axis='both',direction='in',which='minor',
               length=3,width=.5,labelsize=fontsize)
ax.tick_params(axis='both',direction='in',which='major',
               length=5,width=1,labelsize=fontsize)
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
    
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(1.2)

ax.set_xlabel(xlabel,fontsize=fontsize)
ax.set_ylabel(ylabel,fontsize=fontsize)

AA=pd.read_csv(folder+'\Figura_3b.csv')

x=np.arange(100, 3000, 10)
colores=['darkred','darkorange','green','darkblue']
list(mcolors.TABLEAU_COLORS)
for i in range(0,len(Fotometros_N)):
    if i<4:
        ax2.plot(x,Smooth(30,AA[Fotometros_N[i]].values/2),linewidth=1.5,color=colores[i],alpha=.9,label=Fotometros_N[i])
    else:
        ax2.plot(x[:100],Smooth(30,AA[Fotometros_N[i]].values[:100]/2),linewidth=1.5,color=colores[i-4],linestyle='--',alpha=.9,label=Fotometros_N[i])
ax2.axvline(x=500, color="red",linewidth=1.2,linestyle='-',alpha=1)
ax2.text(380,-0.0014,'500',fontsize=12,multialignment='center')

ax2.legend(loc='upper right',fontsize=11)

ax2.minorticks_on()
ax2.tick_params(axis='both',direction='in',which='minor',
               length=3,width=.5,labelsize=fontsize)
ax2.tick_params(axis='both',direction='in',which='major',
               length=5,width=1,labelsize=fontsize)
ax2.yaxis.set_ticks_position('both')
ax2.xaxis.set_ticks_position('both')
    
for axis in ['top','bottom','left','right']:
    ax2.spines[axis].set_linewidth(1.2)

ax2.set_xlabel(xlabel2,fontsize=fontsize)
ax2.set_ylabel(ylabel2,fontsize=fontsize)

plt.tight_layout()
plt.show()