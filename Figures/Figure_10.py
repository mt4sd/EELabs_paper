import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import argparse

#Input of the script
parser = argparse.ArgumentParser()
parser.add_argument('--folder_data',  type=str,required=True,  help='Folder where the CSV files of the figures are located')
args = parser.parse_args()

folder = args.folder_data

A=pd.read_csv(folder+'\Figura_10.csv')

A=A[A['DNB_BRDF_Corrected_NTL_log_P50']>-0.7]
B=A[A['Descartados']==True]
A=A[A['Descartados']==False]

def CORREGIR(a):
    return np.log10(np.e**a)

fig = plt.figure(1, figsize=(10,6))
plt.clf()
ax = plt.subplot(111)
xlabel = r'P50$_{\mathrm{log (VIIRS)}}$ [log(nW/(cm$^{2}$sr))]'
ylabel = r'P50$_{ \mathrm{TESS\ and\ SG}}$ [mag/arcsec$^{2}$]'
UN=A[np.invert(A['name'].str.contains(','))]
VARIOS=A[A['name'].str.contains(',')]


E_X=[np.abs(UN['Ext_fot_izq'].values-UN['P50_fot'].values),np.abs(UN['Ext_fot_der'].values-UN['P50_fot'].values)]
E_Y=[np.abs(UN['Ext_sat_izq'].values-UN['DNB_BRDF_Corrected_NTL_log_P50'].values),np.abs(UN['Ext_sat_der'].values-UN['DNB_BRDF_Corrected_NTL_log_P50'].values)]

E_X2=[np.abs(VARIOS['Ext_fot_izq'].values-VARIOS['P50_fot'].values),np.abs(VARIOS['Ext_fot_der'].values-VARIOS['P50_fot'].values)]
E_Y2=[np.abs(VARIOS['Ext_sat_izq'].values-VARIOS['DNB_BRDF_Corrected_NTL_log_P50'].values),np.abs(VARIOS['Ext_sat_der'].values-VARIOS['DNB_BRDF_Corrected_NTL_log_P50'].values)]

ax.errorbar(x=UN['DNB_BRDF_Corrected_NTL_log_P50'].values,y=UN['P50_fot'].values,xerr=E_Y,yerr=E_X,capsize=1.5, fmt='none',barsabove=True,elinewidth=1,ecolor='black',label=r'Photometers')
ax.errorbar(x=VARIOS['DNB_BRDF_Corrected_NTL_log_P50'].values,y=VARIOS['P50_fot'].values,xerr=E_Y2,yerr=E_X2,capsize=1.5, fmt='none',barsabove=True,elinewidth=1,ecolor='blue',label=r'Group of photometers in the same pixel')
ax.scatter(x=B['DNB_BRDF_Corrected_NTL_log_P50'].values,y=B['P50_fot'].values,color='red',s=80,marker='2',label=r'Discarded photometers')
ax.plot(np.linspace(-2,3),-0.9497474472911072*np.linspace(-2,3)+20.929127435594243,linestyle='--',linewidth=1,color='black')


ax.legend(loc='lower right',fontsize=11)

ax.set_xlim(-1.1,2.5)
ax.set_ylim(17.3,22)

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

ax.invert_yaxis()

plt.tight_layout()
plt.show()