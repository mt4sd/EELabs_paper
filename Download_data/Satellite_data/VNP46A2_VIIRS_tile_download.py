#EELab enviroment
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
parser.add_argument('--left_upper_corner',  required=True, type=str, help='Format example [longitude,latitude]: [-18,28]')
parser.add_argument('--right_lower_corner',  required=True, type=str, help='Format example [longitude,latitude]: [-17,29]')
parser.add_argument('--day_from',  type=int, help='Day from, day of the year number, between 1 and 365')
parser.add_argument('--day_to',  type=int, help='Day to, day of the year number, between 1 and 365')
parser.add_argument('--out','--output', required=True, type=str, help='Output filename')
parser.add_argument('--token', required=True, type=str, help='NASA EARTHDATA token. Please visit the link https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5000/VNP46A4/2021/001/. If necessary, register an account. It is important to have an active user account to proceed. Click on -See wget Download command- to obtain the token. If there is not a token, download a file and click on it again. The token expires every 4-6 months.')
args = parser.parse_args()

year_from=args.year_from
year_to=args.year_to
day_from=args.day_from
day_to=args.day_to
output=args.out
left_upper_corner=args.left_upper_corner
right_lower_corner=args.right_lower_corner
token=args.token



left_upper_corner=left_upper_corner[1:-1].split(',')
right_lower_corner=right_lower_corner[1:-1].split(',')

#Function to identify the tile of the coordinate
def Tile(lon,lat):
    v=np.floor((90-lat)/10)
    h=np.floor((lon+180)/10)
    return int(v),int(h)
left_upper_tile=Tile(float(left_upper_corner[0]),float(left_upper_corner[1]))
right_lower_tile=Tile(float(right_lower_corner[0]),float(right_lower_corner[1]))


#Function that adds zeros to numbers on the left side if they are less than 10, according to the notation of the quadrants
def Add_zero(a):
    if a<10:
        return ('0'+str(a))
    else:
        return str(a)

#Function for format day: 1->001, 23->023, 124->124
def format_day(day):
    if day<10:
        return '00'+str(day)
    elif day<100:
        return '0'+str(day)
    else:
        return str(day)
    
quadrants=[]
for i in range(left_upper_tile[0],right_lower_tile[0]+1):
    for ii in range(left_upper_tile[1],right_lower_tile[1]+1):
        quadrants=quadrants+['h'+Add_zero(ii)+'v'+Add_zero(i)]

#Obtain the list of files for the quadrants that need to be downloaded for a specific day and year.
def File_name(year,day,product):
    day=format_day(day)
    csv=pd.read_csv('https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5000/'+product+'/'+str(year)+'/'+day+'.csv')
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

def Download(year,day,product):
    A=set(File_name(year,day,product))
    url='https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5000/'+product+'/'+str(year)+'/'+format_day(day) 
    out=output+'/year_'+str(year)+'/day_'+format_day(day)
    os.makedirs(out, exist_ok=True)
    sync(url,out,token,A)

grid_width=15/60/60
grid=np.array(range(0,2400))*grid_width

#Function to check if the position goes out of bounds of the grid
def Out(a):
    if a<0 or a>=2400:
        return None
    else:
        return a

def Download_processing(year,day):
    
    Download(year,day,'VNP46A1')
    
    folder=output+'/year_'+str(year)+'/day_'+format_day(day)
    files=os.listdir(folder)
    Data=pd.DataFrame()
    for ii in files:
        h5file = h5py.File(folder+"/"+ii,"r")
        quadrant=ii.split('.')[2]
        h=quadrant[1:3]
        v=quadrant[4:6]
    
        Pos_1_sd=int(np.round((-float(left_upper_corner[1])+(90-int(v)*10))/grid_width))
        Pos_2_sd=int(np.round((float(left_upper_corner[0])-(-180+int(h)*10))/grid_width))
        Pos_1_ii=int(np.round((-float(right_lower_corner[1])+(90-int(v)*10))/grid_width))
        Pos_2_ii=int(np.round((float(right_lower_corner[0])-(-180+int(h)*10))/grid_width))

        Pos_1_sd=Out(Pos_1_sd)
        Pos_2_sd=Out(Pos_2_sd)
        Pos_1_ii=Out(Pos_1_ii)
        Pos_2_ii=Out(Pos_2_ii)

        lon=-180+int(h)*10
        lat=90-int(v)*10
        LON=np.array(2400*list(lon+grid)).reshape(2400,2400)
        LAT=np.transpose(np.array(2400*list(lat-grid)).reshape(2400,2400))
        
        var1=np.array(h5file['HDFEOS']['GRIDS']['VNP_Grid_DNB']['Data Fields']['DNB_At_Sensor_Radiance_500m'])
        var2=np.array(h5file['HDFEOS']['GRIDS']['VNP_Grid_DNB']['Data Fields']['QF_Cloud_Mask'])
        var3=np.array(h5file['HDFEOS']['GRIDS']['VNP_Grid_DNB']['Data Fields']['UTC_Time'])

        Data['lon']=LON[Pos_1_sd-1:Pos_1_ii+1,Pos_2_sd-1:Pos_2_ii+1].reshape(1,-1)[0]
        Data['lat']=LAT[Pos_1_sd-1:Pos_1_ii+1,Pos_2_sd-1:Pos_2_ii+1].reshape(1,-1)[0]
        Data['DNB_At_Sensor_Radiance_500m']=var1[Pos_1_sd-1:Pos_1_ii+1,Pos_2_sd-1:Pos_2_ii+1].reshape(1,-1)[0]
        Data['QF_Cloud_Mask']=var2[Pos_1_sd-1:Pos_1_ii+1,Pos_2_sd-1:Pos_2_ii+1].reshape(1,-1)[0]
        
        Data['UTC_Time']=var3[Pos_1_sd-1:Pos_1_ii+1,Pos_2_sd-1:Pos_2_ii+1].reshape(1,-1)[0]
        
        Data['DNB_At_Sensor_Radiance_500m']=Data['DNB_At_Sensor_Radiance_500m'].replace({65535:np.nan})*0.1 
        Data['UTC_Time']=Data['UTC_Time'].replace({-999.9:np.nan})
        
        hour=np.floor(Data['UTC_Time'])
        minutes=np.floor((Data['UTC_Time']-hour)*60)
        seconds=((Data['UTC_Time']-hour)*60-minutes)*60
        
        Data['Date']=datetime.strptime(str(year)+','+str(day),'%Y,%j')
        Dates=[]
        for i in range(0,len(Data)):

            try:
                date=datetime(Data['Date'][i].year,Data['Date'][i].month,Data['Date'][i].day, int(hour[i]),int(minutes[i]),int(seconds[i]))
            except:
                date=np.nan
            Dates=Dates+[date]
        Data['Date_UTC']=Dates
        Data.drop(['UTC_Time'],axis=1)
        
        QF_Cloud_Mask=Data['QF_Cloud_Mask'].fillna(65535) 
        QF_Cloud_Mask=["{:16b}".format(int(i)).replace(' ','0') for i in QF_Cloud_Mask] 
        Nulls=list(np.where(np.array(QF_Cloud_Mask)=='1111111111111111')[0]) 
    
        Cloud_Detection_Results=[i[6:8] for i in QF_Cloud_Mask]
        Shadow_Detected=[i[8] for i in QF_Cloud_Mask]
        Cirrus_Detection=[i[9] for i in QF_Cloud_Mask]
        
        for i in Nulls:
            Cloud_Detection_Results[i]=np.nan
            Shadow_Detected[i]=np.nan
            Cirrus_Detection[i]=np.nan

        Data['Cloud_Detection_Results']=Cloud_Detection_Results
        Data['Shadow_Detected']=Shadow_Detected
        Data['Cirrus_Detection']=Cirrus_Detection
        Data['Cloud_Detection_Results']=Data['Cloud_Detection_Results'].replace({'00':'Confident_clear','01':'Probably_clear','10':'Probably_cloudy','11':'Confident_cloudy'})
        Data['Shadow_Detected']=Data['Shadow_Detected'].replace({'0':'No','1':'Yes'}) 
        Data['Cirrus_Detection']=Data['Cirrus_Detection'].replace({'0':'No_cloud','1':'Cloud'}) 
        Data.replace({None:np.nan})

        Data=Data.drop(['QF_Cloud_Mask'], axis=1)

    rmtree(folder)
    Download(year,day,'VNP46A2')
    folder=output+'/year_'+str(year)+'/day_'+format_day(day)
    files=os.listdir(folder)    
    for ii in files:
        h5file = h5py.File(folder+"/"+ii,"r")
        quadrant=ii.split('.')[2]
        h=quadrant[1:3]
        v=quadrant[4:6]
    
        Pos_1_sd=int(np.round((-float(left_upper_corner[1])+(90-int(v)*10))/grid_width))
        Pos_2_sd=int(np.round((float(left_upper_corner[0])-(-180+int(h)*10))/grid_width))
        Pos_1_ii=int(np.round((-float(right_lower_corner[1])+(90-int(v)*10))/grid_width))
        Pos_2_ii=int(np.round((float(right_lower_corner[0])-(-180+int(h)*10))/grid_width))

        Pos_1_sd=Out(Pos_1_sd)
        Pos_2_sd=Out(Pos_2_sd)
        Pos_1_ii=Out(Pos_1_ii)
        Pos_2_ii=Out(Pos_2_ii)
   
        var1=np.array(h5file['HDFEOS']['GRIDS']['VNP_Grid_DNB']['Data Fields']['DNB_BRDF-Corrected_NTL'])
        var2=np.array(h5file['HDFEOS']['GRIDS']['VNP_Grid_DNB']['Data Fields']['Gap_Filled_DNB_BRDF-Corrected_NTL'])

        Data['DNB_BRDF-Corrected_NTL']=var1[Pos_1_sd-1:Pos_1_ii+1,Pos_2_sd-1:Pos_2_ii+1].reshape(1,-1)[0]
        Data['Gap_Filled_DNB_BRDF-Corrected_NTL']=var2[Pos_1_sd-1:Pos_1_ii+1,Pos_2_sd-1:Pos_2_ii+1].reshape(1,-1)[0]
    
        Data['DNB_BRDF-Corrected_NTL']=Data['DNB_BRDF-Corrected_NTL'].replace({65535:np.nan})*0.1
        Data['Gap_Filled_DNB_BRDF-Corrected_NTL']=Data['Gap_Filled_DNB_BRDF-Corrected_NTL'].replace({65535:np.nan})*0.1
        Data.replace({None:np.nan})
    rmtree(folder)
    Data['Date']=datetime.strptime(str(year)+','+str(day),'%Y,%j')
    return Data

def DOWNLOAD_PROCESSING(year_from,year_to,day_from=1,day_to=365):
    #Check until which day and year the data has already been downloaded
    try:
        Records=pd.read_csv(output+"/Data_tile_VIIRS.csv")
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
                Records=pd.read_csv(output+"/Data_tile_VIIRS.csv")
            except:
                Records=pd.DataFrame()
            success=False
            
            while success==False:
                try:
                    Dataset=Download_processing(i,ii)
                    success=True
                except:
                    success=False
            New_records=pd.concat([Records,Dataset])
            New_records.to_csv(output+"/Data_tile_VIIRS.csv", index = False)

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

