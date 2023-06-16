#Pasos a seguir:
#1) Installar el repostorio de proyecto EELabs, con .env  y credentials.json en \resources_folder\google, y el entorno conda
#2) Pegar este script en dentro del repositorio \
#3) Ejecutar desde su ubicacion
#IMPORTANTE no permite realizar actualizaciones de fecha, está pensado para una descarga única no para realizar descargas actualizadas
import select
from utils.devices_api.eelabs_devices_api import EELabsDevicesApi
from utils.devices.tess import TESS
from utils.devices.skyglow import SkyGlow
from utils.devices.sqm import SQM
from utils.devices.astmon import ASTMON
import pandas as pd
import numpy as np
from datetime import datetime
from utils.my_utils import Utils

import config as conf #Configuration variables
from utils.filter import Filter
from datetime import date

import argparse
import os

#Input of the script
parser = argparse.ArgumentParser()
parser.add_argument('--f', '--from',  type=int, help='Year from')
parser.add_argument('--to',  type=int, help='Year to')
parser.add_argument('--out','--output', required=True, type=str, help='Output filename')
parser.add_argument('--filter', type=str, help='Data filtering: sun, moon, clouds, galaxy, zodiacal, sigma. Format example: [sun,galaxy,zodaical] Write all without brackets for all filters. Format example: all')
parser.add_argument('--device',type=str,help='Format exalmple: [LPL1_001,LPL2_033,stars1] rite all without brackets for ones device. Format example: stars1')
parser.add_argument('--ephemeris',type=bool,help='True for ephemeris included')
args = parser.parse_args()

initial_year = args.f
final_year = args.to
output = args.out
filter = args.filter
ephemerides = args.ephemeris
if filter:
    if filter[0]=='[':
        filter=filter[1:-1].split(',')
    else:
        filter=filter
else:
    filter=[]
select_devices=args.device
if select_devices:
    if select_devices[0]=='[':
        select_devices=set(select_devices[1:-1].split(','))
    else:
        select_devices=set([select_devices])


#Create the save folder
output=output+'\Photometer_data'
if not os.path.exists(output):
    os.mkdir(output)


#Photometers dataset
devices=EELabsDevicesApi().get_all_devices_info()
devices=pd.DataFrame(devices)
devices=devices.drop(['sg_type','lpl','zero_point','filters','mov_sta_position','local_timezone','location','info_img','info_tess','place','tester','info_org','__v','latitude','longitude','country','city'],axis=1)
localizacion=pd.DataFrame(list(devices['info_location'])).drop(['latitude_hide','longitude_hide'],axis=1)
devices['place']=localizacion['place']
devices['town']=localizacion['town']
devices['sub_region']=localizacion['sub_region']
devices['region']=localizacion['region']
devices['country']=localizacion['country']
devices['latitude']=localizacion['latitude']
devices['longitude']=localizacion['longitude']
devices['elevation']=localizacion['elevation']
devices=devices.drop(['info_location'],axis=1)
devices.to_csv(output+'\All_devices.csv', index = False)

#Folder to save records
if not os.path.exists(output+'\Records'):
    os.mkdir(output+'\Records')



#Obtain the device class regardless of its type
def Device(device_name): 
    devices=pd.read_csv(output+'\All_devices.csv')
    type=devices[devices['name']==device_name]['TYPE'].values[0]
    if type==TESS.TYPE:
        device_obj=TESS(name=device_name)
    elif type==SkyGlow.TYPE:
        device_obj=SkyGlow(name=device_name)
    elif type==SQM.TYPE:
        device_obj=SQM(name=device_name)
    elif type==ASTMON.TYPE:
        device_obj=ASTMON(name=device_name)
    return device_obj
#Obtain filtered data for a device and year
def Data(device_name,year,filter): #filter: data vector such as ['sun', 'moon'] for example.
    device_obj=Device(device_name)
    FIRST_DATE=pd.Timestamp(datetime(year, 1, 1, 0, 0), tz='UTC')
    LAST_DATE=pd.Timestamp(datetime(year+1, 1, 1, 0, 0), tz='UTC')
    df_all=None
    try:
        df_all = device_obj.get_all_data(date_from=FIRST_DATE, date_to=LAST_DATE,force=False)
        No_data=False
    except:
        df_all=None
        No_data=True
    if No_data:
        print('The device '+device_name+' not responded due to an error')
    df_all=df_all[(df_all['mag']>conf.MAG_MIN) & (df_all['mag']<conf.MAG_MAX)] #Filter for extreme magnitudes
    if __name__ == '__main__':
        df_all = Utils().add_ephems(df_all, device_obj.getObserver(), parallelize=False) # The parallelize option is causing issues
    V=[]
    if 'sun' in filter or filter=='all':
        df_all = Filter().filter_sun(df_all, max_sun_alt=conf.SUN_ALT_MAX)
    else:
        df_filter=Filter().filter_sun(df_all, max_sun_alt=conf.SUN_ALT_MAX)
        F=np.array([True]*(df_all.index[-1]+1)) #Vector with all True for all indices
        F[df_filter.index]=False #Replace remaining indices to False after filtering
        df_all['sun']=F[df_all.index] #Retrieve data according to the original index
        V=V+['sun']
    if 'moon' in filter or filter=='all':
        df_all = Filter().filter_moon(df_all, max_moon_alt=conf.MOON_ALT_MAX)
    else:
        df_filter=Filter().filter_moon(df_all, max_moon_alt=conf.MOON_ALT_MAX)
        F=np.array([True]*(df_all.index[-1]+1))
        F[df_filter.index]=False
        df_all['moon']=F[df_all.index]
        V=V+['moon']
    if 'clouds' in filter or filter=='all':
        clouds_threshold=conf.CLOUD_STD_FREQ
        df_all = Filter().filter_column(df_all, device_obj.getMagSTDColname(), max=clouds_threshold)
    else:
        clouds_threshold=conf.CLOUD_STD_FREQ
        df_filter=Filter().filter_column(df_all, device_obj.getMagSTDColname(), max=clouds_threshold)
        F=np.array([True]*(df_all.index[-1]+1))
        F[df_filter.index]=False
        df_all['clouds']=F[df_all.index]
        V=V+['clouds']
    if 'galaxy' in filter or filter=='all':
        df_all = Filter().filter_galactic_abs_lat(df_all, min_lat=conf.GALACTIC_LAT_MIN, max_lat=180)
    else:
        df_filter=Filter().filter_galactic_abs_lat(df_all, min_lat=conf.GALACTIC_LAT_MIN, max_lat=180)
        F=np.array([True]*(df_all.index[-1]+1))
        F[df_filter.index]=False
        df_all['galaxy']=F[df_all.index]
        V=V+['galaxy']
    if 'zodiacal' in filter or filter=='all':
        df_all = Filter().filter_column(df_all, col_name='ecliptic_f', max=conf.ECLIPTIC_F_MAX)
    else:
        df_filter=Filter().filter_column(df_all, col_name='ecliptic_f', max=conf.ECLIPTIC_F_MAX)
        F=np.array([True]*(df_all.index[-1]+1))
        F[df_filter.index]=False
        df_all['zodiacal']=F[df_all.index]
        V=V+['zodiacal']
    if 'sigma' in filter or filter=='all':
        sigma=conf.NSIGMA
        df_all = Filter().filter_nsigma(df_all, col_name='mag', sigma=sigma)
    else:
        sigma=conf.NSIGMA
        df_filter=Filter().filter_nsigma(df_all, col_name='mag', sigma=sigma)
        F=np.array([True]*(df_all.index[-1]+1))
        F[df_filter.index]=False
        df_all['sigma']=F[df_all.index]
        V=V+['sigma'] 
    if ephemerides:
        df=pd.DataFrame({'time':df_all['time'],'mag':df_all['mag'],'name':device_name,'moon_phase':df_all['moon_phase'],'moon_alt':df_all['moon_alt'],'galactic_lat':df_all['galactic_lat'],'galactic_lon':df_all['galactic_lon'],'helioecliptic_lon_abs':df_all['helioecliptic_lon_abs'],'ecliptic_lat_abs':df_all['ecliptic_lat_abs']})
    else:
        df=pd.DataFrame({'time':df_all['time'],'mag':df_all['mag'],'name':device_name})
    for ii in V:
        df[ii]=df_all[ii]
    return df
#Obtain all data between two years
def Data_download(V,initial_year=None,final_year=None,iterate=True): #Iterate to prompt for enter key per iteration
    #Downloaded devices
    Downloaded_devices=set()
    for j in range(0,1000):
        try:
            df_records=pd.read_csv(output+'\Records\Records_'+str(j)+'.csv')
            Downloaded_devices=Downloaded_devices|set(df_records['name'])
        except:
            Downloaded_devices=Downloaded_devices

    #Log devices
    try:
        df_log=pd.read_csv(output+'\Log.csv')
        Log_devices=set(df_log['Devices'])
        Log_exists=True
    except:
        Log_devices=set()
        Log_exists=False
    diff=Downloaded_devices-Log_devices
    Downloaded_devices=Downloaded_devices|Log_devices
    print(Downloaded_devices)
    df_all_devices=pd.read_csv(output+'\All_devices.csv')
    All_devices=set(df_all_devices['name'])
    if select_devices:
        Missing_devices=select_devices-Downloaded_devices
    else:
        Missing_devices=All_devices-Downloaded_devices #To know which devices need to be download
    n_missing_devices=len(Missing_devices)
    if initial_year:
        i_year=initial_year
    else:
        i_year=2010
    if final_year:
        f_year=final_year
    else:
        f_year=date.today().year
 
    Downloaded_missing_devices=[]
    v_empty=[]
    v_time=[]
    #Loop where it goes device by device and then year by year
    for i in Missing_devices:
        df=pd.DataFrame()
        empty=True
        for ii in range(i_year,f_year+1): 
            try:
                dat=Data(i,ii,V)
                df=pd.concat([df,dat])
                if list(dat.values)!=[]:
                    empty=False
            except:
                df=df
            print('Year: '+str(ii))
        #Save
        #Saving with files limited to 1 GB
        try:
            df_records=pd.read_csv(output+'\Records\Records_1.csv')
            Records_exist=True
        except:
            df_final=df
            df_final.to_csv(output+'\Records\Records_1.csv', index = False)
            Records_exist=False
        if Records_exist==True:
            counter=0
            for j in range(1,1000):    
                try:
                    df_records=pd.read_csv(output+'\Records\Records_'+str(j)+'.csv')
                    if os.stat(output+'\Records\Records_'+str(j)+'.csv').st_size<1000000000:
                        df_final=pd.concat([df_records,df])
                        df_final.to_csv(output+'\Records\Records_'+str(j)+'.csv', index = False)
                        counter=1
                except:
                    if counter==0:
                        df_final=df
                        df_final.to_csv(output+'\Records\Records_'+str(j)+'.csv', index = False)
                        counter=1

        time=datetime.now()
        v_empty=v_empty+[empty]
        v_time=v_time+[time]
        Downloaded_missing_devices=Downloaded_missing_devices+[i]

        Log_downloaded_devices=pd.DataFrame({'Devices':Downloaded_missing_devices,'Time':v_time,'Empty':v_empty})
        Log_downloaded_devices_2=pd.DataFrame({'Devices':list(diff),'Time':None,'Empty':False})
        Log=pd.concat([Log_downloaded_devices_2,Log_downloaded_devices])
        #Save log
        if Log_exists:
            Log_2=pd.concat([df_log,Log])
        else:
            Log_2=Log
        Log_2.to_csv(output+'\Log.csv', index = False)       
        n_no_downloaded_missing_devices=n_missing_devices-len(Downloaded_missing_devices)
        print(str(n_no_downloaded_missing_devices)+' are still pending for download')
        if iterate:
            if input('Downloaded device:'+i+'\n')=='exit': 
                break
        else:
            print('Downloaded device:'+i+'\n')
#Run
Data_download(filter,initial_year,final_year,iterate=False)


