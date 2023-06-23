**VNP46A2_VIIRS_DOWNLOAD.PY DESCRIPTION**

VNP46A2_VIIRS_download.py is a script to download data from VIIRS satellite in the photometers' location, NASA product VNP46A2. IT IS NOT TO UPDATE DOWNLOADED DATA. It requires the Download_VIIRS.yml environment. 

Inputs:

--out, --output Folder name and ubication where you want to save the data. Example: C:\Users\borja\Downloads\Folder REQUIRED INPUT

--photometers File path of the All_devices.csv file created by Download_EELabs_photometers.py Example: C:\Users\borja\Downloads\All_devices.csv  REQUIRED INPUT

--token NASA EARTHDATA token. Please visit the link https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5000/VNP46A4/2021/001/. 
If necessary, register an account. It is important to have an active user account to proceed. Click on 'See wget Download command' to obtain the token. If there is not a token, download a file and click on it again. 
The token expires every 4-6 months. REQUIRED INPUT

--year_from Year of the start of the downloaded data. REQUIRED INPUT
--year_to Year of the end of the downloaded data. REQUIRED INPUT


--day_from Year of the start of the downloaded data. Day of the year number, between 1 and 365

--day_from Year of the start of the downloaded data. Day of the year number, between 1 and 365


The script will create a Satellite_records.csv. Dataset fields: The name of the photometer, measurement date and VIIRS' fields. These are explained in VIIRS_Black_Marble_UG_v1.2_April_2021.pdf.

IMPORTANT: In case of interrupting the program execution, it can be relaunched to continue the download from where it left off. 
If there are days when VIIRS lacks data, restart the program from the day it resumes having data

**VNP46A2_VIIRS_TILE_DOWNLOAD.PY DESCRIPTION**

VNP46A2_VIIRS_tile_download.py is a script to download data from VIIRS satellite of a coordinate area, NASA product VNP46A2. IT IS NOT TO UPDATE DOWNLOADED DATA. It requires the EELabs environment. 

Inputs:

--out, --output Folder name and ubication where you want to save the data. Example: C:\Users\borja\Downloads\Folder REQUIRED INPUT

--left_upper_corner: Coordinates of the left upper corner of the area. Format example [longitude,latitude]: [-18,28] REQUIRED INPUT

--right_lower_corner: Coordinates of the right lower corner of the area. Format example [longitude,latitude]: [-17,29] REQUIRED INPUT

--token NASA EARTHDATA token. Please visit the link https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5000/VNP46A4/2021/001/. 
If necessary, register an account. It is important to have an active user account to proceed. Click on 'See wget Download command' to obtain the token. If there is not a token, download a file and click on it again. 
The token expires every 4-6 months. REQUIRED INPUT

--year_from Year of the start of the downloaded data. REQUIRED INPUT
--year_to Year of the end of the downloaded data. REQUIRED INPUT


--day_from Year of the start of the downloaded data. Day of the year number, between 1 and 365

--day_from Year of the start of the downloaded data. Day of the year number, between 1 and 365


The script will create a Data_tile_VIIRS.csv. Dataset fields: Logitude, latitude, measurement date and VIIRS' fields. These are explained in VIIRS_Black_Marble_UG_v1.2_April_2021.pdf.

IMPORTANT: In case of interrupting the program execution, it can be relaunched to continue the download from where it left off. 
If there are days when VIIRS lacks data, restart the program from the day it resumes having data

IMPORTANT: Inputs for Valverde de Burguillos map: --left_upper_corner [-18.060,28.893] --right_lower_corner [-17.634,28.410]
