# ---------------------------------------------------------------------------
# hydro_download.py
#
# Description: Downloads all data for hydrology processing from USGS. Unzips data
#              and stores it in an Download folder in the workspace folder used. Also
#              performs download and unzip of all ESU data from NOAA. Completes external
#              download and unzip of data by pulling critical habitat data from FWS.
#              Note: usage is limited to ArcGIS 10.x because of Python version issues with Pro.
#                    Due to the usage of urllib module. Will need to change for Pro.
#
# Runtime Estimates: 13 min 10 sec
#
# Created by: Josh Klaus 08/24/2017 jklaus@fs.fed.us
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import sys
import os
import datetime
import urllib
import zipfile

# Set workspace or obtain from user input
# in_workspace = "C:\\Users\\jklaus\\Documents\\Python_Testing\\fire_retardant\\"
in_workspace = sys.argv[1]

arcpy.env.workspace = in_workspace
arcpy.env.overwriteOutput = True

subRegionList = ["1503", "1604", "1605", "1606", "1710", "1712",
                 "1801", "1802", "1803", "1804", "1805", "1806",
                 "1807", "1808", "1809", "1810"]

salmonList = ["chinook", "coho", "steelhead"]

downloadFolders = ["NOAA_ESU", "Hydro", "CHab"]

downloadPath = in_workspace + "\\" + "Downloads"
if not os.path.exists(downloadPath):
    arcpy.AddMessage("Creating directory for Downloads")
    os.makedirs(downloadPath)

for folder in downloadFolders:

    if not os.path.exists(downloadPath + "\\" + folder):
        arcpy.AddMessage("Creating download directory for " + folder)
        os.makedirs(downloadPath + "\\" + folder)

try:
    arcpy.AddMessage("_____________________________________________________")
    arcpy.AddMessage("Downloading and unzipping all NHD data from USGS ftp site")

    for region in subRegionList:

        filename = "NHD_H_" + region + "_GDB.zip"

        hydroDownloadPath = downloadPath + "\\" + "Hydro"

        downloadFile = os.path.join(hydroDownloadPath, filename)

        url = "ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Hydrography/NHD/HU4/HighResolution/GDB/" + filename

        arcpy.AddMessage("Downloading " + filename + " to " + hydroDownloadPath)

        urllib.urlretrieve(url, downloadFile)

        arcpy.AddMessage("Unzipping " + filename)
        zip_ref = zipfile.ZipFile(downloadFile, 'r')
        zip_ref.extractall(hydroDownloadPath)
        zip_ref.close()

    arcpy.AddMessage("_____________________________________________________")
    arcpy.AddMessage("Downloading and unzipping all ESU data from NOAA website")

    for salmon in salmonList:

        filename = salmon + "_salmon.zip"

        noaaDownloadPath = downloadPath + "\\" + "NOAA_ESU"

        downloadFile = os.path.join(noaaDownloadPath, filename)

        url = "http://www.westcoast.fisheries.noaa.gov/publications/gis_maps/gis_data/salmon_steelhead/esu/" + filename

        arcpy.AddMessage("Downloading " + filename + " to " + noaaDownloadPath)

        urllib.urlretrieve(url, downloadFile)

        arcpy.AddMessage("Unzipping " + filename)
        zip_ref = zipfile.ZipFile(downloadFile, 'r')
        zip_ref.extractall(noaaDownloadPath)
        zip_ref.close()

    arcpy.AddMessage("_____________________________________________________")
    arcpy.AddMessage("Downloading and unzipping all Critical Habitat data from FWS website")
    filename = "crithab_all_layers.zip"

    chabDownloadPath = downloadPath + "\\" + "CHab"

    downloadFile = os.path.join(chabDownloadPath, filename)

    url = "https://ecos.fws.gov/docs/crithab/crithab_all/" + filename

    arcpy.AddMessage("Downloading " + filename + " to " + chabDownloadPath)

    urllib.urlretrieve(url, downloadFile)

    arcpy.AddMessage("Unzipping " + filename)
    zip_ref = zipfile.ZipFile(downloadFile, 'r')
    zip_ref.extractall(chabDownloadPath)
    zip_ref.close()


except arcpy.ExecuteError:
    arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
    arcpy.AddMessage(e)