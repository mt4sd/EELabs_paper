DOWNLOAD_EELABS_PHOTOMETERS.PY DESCRIPTION

Download_EELabs_photometers.py is a script to download data from EELabs photometers. IT IS NOT TO UPDATE DOWNLOADED DATA. It 
requires both the installation of the EELabs repository and the corresponding conda environment to function. It has to be located 
within the main folder of the project, "eelabs_portal".

Inputs:
--out, --output Filename where you want to save the data. REQUIRED INPUT

--f, --from : Year from which you want to download the data
--to : Year to which you want to download the data
--filter : If you want the data with sun, moon, etc. to be removed. List of filters: sun, moon, clouds galaxy, zodiacal, sigma. 
Format example: [sun, galaxy, zodiacal] . Write all without brackets for all filters. Format example: all
--device : List of photometers for which you want to download the data. Format exalmple: [LPL1_001,LPL2_033,stars1] Wite all 
without brackets for ones device. Format example: stars1. Do not use this input if you want to download data for all photometers.
--ephemeris True  if you want to include the ephemeris

The script will create a folder named "Photometer data" with everything. Inside, it contains the Log.csv file with the list of 
successfully downloaded photometers and their respective times. Additionally, it contains All_devices.csv with all existing 
photometers along with their location data and installation dates. And the Records folder with the dataset data of the photometers. 
These datasets are grouped into 1 GB CSV files. Dataset features:

-time: Measurement time
-mag: Magnitude
-name: Photometer name
-sun, moon, galaxy, zodical or sigma: True if that data is influenced by that effect. False otherwise
-ephemeris features: moon_phase, moon_alt, galactic_lat, galactic_lon, helioecliptic_lon_abs; ecliptic_lat_abs

IMPORTANT: In case of interrupting the program execution, it can be relaunched to continue the download from where it left off
