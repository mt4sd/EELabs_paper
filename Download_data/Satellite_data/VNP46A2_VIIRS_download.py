#EXAMPLE
#python VNP46A2_VIIRS_download.py --year_from 2022 --year_to 2022 --photometers /mnt/data/datos_borja/Todos_fotometros.csv --out /mnt/data/datos_borja/VIIRS/Diarios_corregidos


#Entorno EELabs
import pandas as pd
import numpy as np 
import h5py
import os
import time
from datetime import datetime
from shutil import rmtree

import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument('--year_from',  required=True, type=int, help='Year from')
parser.add_argument('--year_to',  required=True, type=int, help='Year to')
parser.add_argument('--day_from',  type=int, help='Day from, day of the year number, between 1 and 365')
parser.add_argument('--day_to',  type=int, help='Day to, day of the year number, between 1 and 365')
parser.add_argument('--photometers', required=True, type=str, help=' File path of the All_devices.csv file created by Download_EELabs_photometers.py Example: C:/Users/borja/Downloads/All_devices.csv')
parser.add_argument('--out','--output', required=True, type=str, help='Folder name and ubication where you want to save the data. Example: C:/Users/borja/Downloads/Folder')
parser.add_argument('--token', required=True, type=str, help='NASA EARTHDATA token. Please visit the link https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5000/VNP46A4/2021/001/. If necessary, register an account. It is important to have an active user account to proceed. Click on -See wget Download command- to obtain the token. If there is not a token, download a file and click on it again. The token expires every 4-6 months.')
args = parser.parse_args()

year_from=args.year_from
year_to=args.year_to
day_from=args.day_from
day_to=args.day_to
photometers=args.photometers
output=args.out
token=args.token



#List of photometers
Photometers=pd.read_csv(photometers)

#Obtain the h and v values of the quadrant to which those photometers belong
v=np.floor((90-Photometers['latitude'])/10)
h=np.floor((Photometers['longitude']+180)/10)

#Function that adds zeros to numbers on the left side if they are less than 10, according to the notation of the quadrants
def Add_zero(a):
    if a<10:
        return ('0'+str(a))
    else:
        return str(a)
    
#Get the quadrant with the h and v values.
W=[]
for i, j in zip(h,v):
    a=Add_zero(int(i))
    b=Add_zero(int(j))
    W=W+['h'+a+'v'+b]

#Get he list of quadrants in order
Photometers['Quadrant']=W
quadrants=np.sort(np.array(list(set(Photometers['Quadrant']))))

#Function for format day: 1->001, 23->023, 124->124
def format_day(day):
    if day<10:
        return '00'+str(day)
    elif day<100:
        return '0'+str(day)
    else:
        return str(day)
    
#Obtain the list of files for the quadrants that need to be downloaded for a specific day and year.
def File_name(year,day):
    day=format_day(day)
    csv=pd.read_csv('https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5000/VNP46A2/'+str(year)+'/'+day+'.csv')
    files=[(None if i==[] else i[0]) for i in [[i for i in csv['name'] if ii in i] for ii in quadrants]]
    return files

#FUNCTIONS FOR DOWNLOADING OBTAINED FROM THE NADA WEBSITE, MODIFIED TO DOWNLOAD ONLY SPECIFIC FILES INSTEAD OF THE ENTIRE DATASET AS INDICATED BY NADA
#from __future__ import (division, print_function, absolute_import, unicode_literals)
import argparse
import os
import os.path
import shutil
import sys
from io import StringIO       

USERAGENT = 'tis/download.py_1.0--' + sys.version.replace('\n','').replace('\r','')


def geturl(url, token=None, out=None):
    headers = { 'user-agent' : USERAGENT }
    if not token is None:
        headers['Authorization'] = 'Bearer ' + token
    try:
        import ssl
        CTX = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        if sys.version_info.major == 2:
            import urllib2
            try:
                fh = urllib2.urlopen(urllib2.Request(url, headers=headers), context=CTX)
                if out is None:
                    return fh.read()
                else:
                    shutil.copyfileobj(fh, out)
            except urllib2.HTTPError as e:
                print('HTTP GET error code: %d' % e.code(), file=sys.stderr)
                print('HTTP GET error message: %s' % e.message, file=sys.stderr)
            except urllib2.URLError as e:
                print('Failed to make request: %s' % e.reason, file=sys.stderr)
            return None

        else:
            from urllib.request import urlopen, Request, URLError, HTTPError
            try:
                fh = urlopen(Request(url, headers=headers), context=CTX)
                print(fh)
                if out is None:
                    return fh.read().decode('utf-8')
                else:
                    shutil.copyfileobj(fh, out)
            except HTTPError as e:
                print('HTTP GET error code: %d' % e.code(), file=sys.stderr)
                print('HTTP GET error message: %s' % e.message, file=sys.stderr)
            except URLError as e:
                print('Failed to make request: %s' % e.reason, file=sys.stderr)
            return None

    except AttributeError:
        # OS X Python 2 and 3 don't support tlsv1.1+ therefore... curl
        import subprocess
        try:
            args = ['curl', '--fail', '-sS', '-L', '--get', url]
            for (k,v) in headers.items():
                args.extend(['-H', ': '.join([k, v])])
            if out is None:
                # python3's subprocess.check_output returns stdout as a byte string
                result = subprocess.check_output(args)
                return result.decode('utf-8') if isinstance(result, bytes) else result
            else:
                subprocess.call(args, stdout=out)
        except subprocess.CalledProcessError as e:
            print('curl GET error message: %' + (e.message if hasattr(e, 'message') else e.output), file=sys.stderr)
        return None

def sync(src, dest, tok,A):
    '''synchronize src url with dest directory'''
    try:
        import csv
        files = [ f for f in csv.DictReader(StringIO(geturl('%s.csv' % src, tok)), skipinitialspace=True) ]
    except ImportError:
        import json
        files = json.loads(geturl(src + '.json', tok))

    # use os.path since python 2/3 both support it while pathlib is 3.4+
    for f in files:
        print(f['name'])
        if f['name'] in A:
          # currently we use filesize of 0 to indicate directory
          filesize = int(f['size'])
          path = os.path.join(dest, f['name'])
          url = src + '/' + f['name']
          if filesize == 0:
              try:
                  print('creating dir:', path)
                  os.mkdir(path)
                  sync(src + '/' + f['name'], path, tok)
              except IOError as e:
                  print("mkdir `%s': %s" % (e.filename, e.strerror), file=sys.stderr)
                  sys.exit(-1)
          else:
              try:
                  if not os.path.exists(path):
                      print('downloading: ' , path)
                      with open(path, 'w+b') as fh:
                          geturl(url, tok, fh)
                  else:
                      print('skipping: ', path)
              except IOError as e:
                  print("open `%s': %s" % (e.filename, e.strerror), file=sys.stderr)
                  sys.exit(-1)
    return 0

#END OF NASA FUNCTIONS
#USER TOKEN 
#token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJBUFMgT0F1dGgyIEF1dGhlbnRpY2F0b3IiLCJpYXQiOjE2Njc0NjYwOTEsIm5iZiI6MTY2NzQ2NjA5MSwiZXhwIjoxNjgzMDE4MDkxLCJ1aWQiOiJib3JqYWZlcm5hbnJ1aXoiLCJlbWFpbF9hZGRyZXNzIjoiYm9yamFmZXJuYW5ydWl6QGdtYWlsLmNvbSIsInRva2VuQ3JlYXRvciI6ImJvcmphZmVybmFucnVpeiJ9.TlzzZ3cJYwZIAbFQ9tOft_PAIdY_KPsMeeSJThN5Lqg'

#Download a specific year and day
def Download(year,day):
    A=set(File_name(year,day))
    url='https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5000/VNP46A2/'+str(year)+'/'+format_day(day) 
    out=output+'/year_'+str(year)+'/day_'+format_day(day)
    os.makedirs(out, exist_ok=True)
    sync(url,out,token,A)

#A 15-arcsecond grid
grid=15/60/60 #Degree

#Calculation of positions on the grid
Pos_1=np.round((Photometers['longitude']-(-180+h*10))/grid)
Pos_2=np.round((-Photometers['latitude']+(90-v*10))/grid)

Photometers['Pos_1']=Pos_2
Photometers['Pos_2']=Pos_1

#Function that obtains a dataframe with the data of interest for a specific day and year     
def Data_sat(year,day):
    folder=output+'/year_'+str(year)+'/day_'+format_day(day) 
    files=os.listdir(folder)
    Photometers2=Photometers.copy()

#Searches photometer by photometer with the quadrants and positions, collecting values
    for i,r in Photometers.iterrows():
        for ii in files:
            if r['Quadrant'] in ii:
                print(ii)
                h5file = h5py.File(folder+"/"+ii,"r")
                Photometers2.at[i,"DNB_BRDF-Corrected_NTL"]=np.array(h5file['HDFEOS']['GRIDS']['VNP_Grid_DNB']['Data Fields']['DNB_BRDF-Corrected_NTL'])[int(r['Pos_1'])][int(r['Pos_2'])]
                Photometers2.at[i,"Gap_Filled_DNB_BRDF-Corrected_NTL"]=np.array(h5file['HDFEOS']['GRIDS']['VNP_Grid_DNB']['Data Fields']['Gap_Filled_DNB_BRDF-Corrected_NTL'])[int(r['Pos_1'])][int(r['Pos_2'])]
                Photometers2.at[i,"DNB_Lunar_Irradiance"]=np.array(h5file['HDFEOS']['GRIDS']['VNP_Grid_DNB']['Data Fields']['DNB_Lunar_Irradiance'])[int(r['Pos_1'])][int(r['Pos_2'])]
                Photometers2.at[i,"Mandatory_Quality_Flag"]=np.array(h5file['HDFEOS']['GRIDS']['VNP_Grid_DNB']['Data Fields']['Mandatory_Quality_Flag'])[int(r['Pos_1'])][int(r['Pos_2'])]
                Photometers2.at[i,"Latest_High_Quality_Retrieval"]=np.array(h5file['HDFEOS']['GRIDS']['VNP_Grid_DNB']['Data Fields']['Latest_High_Quality_Retrieval'])[int(r['Pos_1'])][int(r['Pos_2'])]
                Photometers2.at[i,"Snow_Flag"]=np.array(h5file['HDFEOS']['GRIDS']['VNP_Grid_DNB']['Data Fields']['Snow_Flag'])[int(r['Pos_1'])][int(r['Pos_2'])]
                Photometers2.at[i,"QF_Cloud_Mask"]=np.array(h5file['HDFEOS']['GRIDS']['VNP_Grid_DNB']['Data Fields']['QF_Cloud_Mask'])[int(r['Pos_1'])][int(r['Pos_2'])]

    DNB_BRDF_Corrected_NTL=Photometers2['DNB_BRDF-Corrected_NTL'].replace({65535:np.nan})*0.1 #Change nulls 
    Gap_Filled_DNB_BRDF_Corrected_NTL=Photometers2['Gap_Filled_DNB_BRDF-Corrected_NTL'].replace({65535:np.nan})*0.1 #Change nulls
    DNB_Lunar_Irradiance=Photometers2['DNB_Lunar_Irradiance'].replace({65535:np.nan})*0.1 #Change nulls
    Mandatory_Quality_Flag=Photometers2['Mandatory_Quality_Flag'].replace({255:np.nan,0:'Alta',1:'Alta',2:'Baja'}) #Change nulls
    Latest_High_Quality_Retrieval_number_days=Photometers2['Latest_High_Quality_Retrieval'].replace({255:np.nan}) #Change nulls
    Snow_Flag=Photometers2['Snow_Flag'].replace({255:np.nan,0:'Sin_nieve',1:'Nieve'}) #Change nulls
    QF_Cloud_Mask=Photometers2['QF_Cloud_Mask'].fillna(65535) #Replace null values with 65535 to avoid errors when working with bits
    QF_Cloud_Mask=["{:16b}".format(int(i)).replace(' ','0') for i in QF_Cloud_Mask] #Convert to binary
    Nulls=list(np.where(np.array(QF_Cloud_Mask)=='1111111111111111')[0]) 
    Day_Night=[i[0] for i in QF_Cloud_Mask]
    Land_Water_Background=[i[1:4] for i in QF_Cloud_Mask]
    Cloud_Mask_Quality=[i[4:6] for i in QF_Cloud_Mask]
    Cloud_Detection_Results=[i[6:8] for i in QF_Cloud_Mask]
    Shadow_Detected=[i[8] for i in QF_Cloud_Mask]
    Cirrus_Detection=[i[9] for i in QF_Cloud_Mask]
    Snow_Surface=[i[10] for i in QF_Cloud_Mask]
    
    for i in Nulls:
        Day_Night[i]=np.nan
        Land_Water_Background[i]=np.nan
        Cloud_Mask_Quality[i]=np.nan
        Cloud_Detection_Results[i]=np.nan
        Shadow_Detected[i]=np.nan
        Cirrus_Detection[i]=np.nan
        Snow_Surface[i]=np.nan
    New_photometros=pd.DataFrame({'name':Photometers2['name'],'DNB_BRDF_Corrected_NTL':DNB_BRDF_Corrected_NTL,'Gap_Filled_DNB_BRDF_Corrected_NTL':Gap_Filled_DNB_BRDF_Corrected_NTL,'DNB_Lunar_Irradiance':DNB_Lunar_Irradiance,'Mandatory_Quality_Flag':Mandatory_Quality_Flag,'Latest_High_Quality_Retrieval_number_days':Latest_High_Quality_Retrieval_number_days,'Snow_Flag':Snow_Flag,'Day_Night':Day_Night,'Land_Water_Background':Land_Water_Background,'Cloud_Mask_Quality':Cloud_Mask_Quality,'Cloud_Detection_Results':Cloud_Detection_Results,'Shadow_Detected':Shadow_Detected,'Cirrus_Detection':Cirrus_Detection,'Snow_Surface':Snow_Surface})    
    New_photometros['Day_Night']=New_photometros['Day_Night'].replace({'0':'Night','1':'Day'}) #Cambio a categorica
    New_photometros['Land_Water_Background']=New_photometros['Land_Water_Background'].replace({'000':'Land_desert','001':'Land_no_desert','010':'Inland_water','011':'Sea_water','101':'Coastal'}) #Cambio a categorica
    New_photometros['Cloud_Mask_Quality']=New_photometros['Cloud_Mask_Quality'].replace({'00':'Poor','01':'Low','10':'Medium','11':'High'})
    New_photometros['Cloud_Detection_Results']=New_photometros['Cloud_Detection_Results'].replace({'00':'Confident_clear','01':'Probably_clear','10':'Probably_cloudy','11':'Confident_cloudy'})
    New_photometros['Shadow_Detected']=New_photometros['Shadow_Detected'].replace({'0':'No','1':'Yes'}) #Cambio a categorica
    New_photometros['Cirrus_Detection']=New_photometros['Cirrus_Detection'].replace({'0':'No_cloud','1':'Cloud'}) #Cambio a categorica
    New_photometros['Snow_Surface']=New_photometros['Snow_Surface'].replace({'0':'No_snow','1':'Snow'}) #Cambio a categorica
    New_photometros.replace({None:np.nan})
    New_photometros['Date']=datetime.strptime(str(year)+','+str(day),'%Y,%j')
    return New_photometros

#Perform the download and processing, returning the dataset for the requested day and year
def Download_processing(year,day):
    folder=output+'/year_'+str(year)+'/day_'+format_day(day)
    success=False
    #It will make as many attempts as necessary to achieve the download.
    while success==False:
        #It will delete those that have been downloaded incorrectly
        try:
            c=os.listdir(folder)
            for i in c:
                if os.stat(folder+'/'+i).st_size==0:
                    os.remove(folder+'/'+i)
        except:
            print('Year: '+str(year)+'    Day: '+str(day))
        try:
            Download(year,day)
            success=True
        except:
            success=False
            time.sleep(1)
            print('There was an error, next attempt')
            f = open (output+'/Errors_log.txt','a')
            date = str(datetime.now())
            f.write('\n'+'There was an error on: '+date)
            f.close()           
    Dataset=Data_sat(year,day)
    rmtree(folder)
    return Dataset

#Download the data between two dates, year, and day of the year
def DOWNLOAD_PROCESSING(year_from,year_to,day_from=1,day_to=365):
    #Check until which day and year the data has already been downloaded
    try:
        Records=pd.read_csv(output+"/Satellite_records.csv")
        Records['Date']=pd.to_datetime(Records['Date'])
        f=max(Records['Date'])
        if (day_from<=int(f.strftime("%j"))):
            day_from=int(f.strftime("%j"))+1
        if (((year_from%4!=0) & (day_from==365)) |((year_from%4==0) & (day_from==366))):
            year_from=f.year+1
            day_from=1
        else:
            year_from=f.year

    except:
        Records=pd.DataFrame()
    for i in range(year_from,year_to+1):
        #To determine if they are leap years
        if i%4==0:
            n=1
        else:
            n=0
        if year_from==year_to:
            day_0=day_from
            day_f=day_to 
        else:
            if i==year_from:
                day_0=day_from
                day_f=365+n
            elif i==year_to:  
                day_0=1
                day_f=day_to  
            else:
                day_0=1
                day_f=365+n
        for ii in range(day_0,day_f+1):
            try:
                Records=pd.read_csv(output+"/Satellite_records.csv")
            except:
                Records=pd.DataFrame()
            Dataset=Download_processing(i,ii)
            New_records=pd.concat([Records,Dataset])
            New_records.to_csv(output+"/Satellite_records.csv", index = False)

if day_from:
    if day_to:
        DOWNLOAD_PROCESSING(year_from,year_to,day_from,day_to)   
    else:
        DOWNLOAD_PROCESSING(year_from,year_to,day_from)
else:
    if day_to:
        DOWNLOAD_PROCESSING(year_from,year_to,1,day_to)
    else:
        DOWNLOAD_PROCESSING(year_from,year_to)

