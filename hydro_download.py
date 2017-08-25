# hydrology_processing.py
#
# Description: Selects out, clips, and buffers hydrology layers for Flowlines,
#              Area, and Waterbody.
# Created by: Josh Klaus 08/24/2017
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import sys
import os
import datetime
import urllib
import urllib2
import zipfile

# Set workspace or obtain from user input
in_workspace = "C:\\Users\\jklaus\\Documents\\Python_Testing\\fire_retardant\\"
# in_workspace = sys.argv[1]

arcpy.env.workspace = in_workspace
arcpy.env.overwriteOutput = True

subRegionList = ["1503", "1604", "1605", "1606", "1710", "1801",
                 "1802", "1803", "1804", "1805", "1806", "1807",
                 "1808", "1809", "1810"]

salmonList = ["chinook", "coho", "steelhead"]

try:
    # for region in subRegionList:
    #
    #     filename = "NHD_H_" + region + "_GDB.zip"
    #
    #     downloadPath = r"C:\Users\jklaus\Documents\Python_Testing\fire_retardant\Downloads\Hydro"
    #
    #     downloadFile = os.path.join(downloadPath, filename)
    #
    #     url = "ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Hydrography/NHD/HU4/HighResolution/GDB/" + filename
    #
    #     arcpy.AddMessage("Downloading " + filename + " to " + downloadPath)
    #
    #     urllib.urlretrieve(url, downloadFile)
    #
    # for salmon in salmonList:
    #
    #     filename = salmon + "_salmon.zip"
    #
    #     downloadPath = r"C:\Users\jklaus\Documents\Python_Testing\fire_retardant\Downloads\NOAA_ESU"
    #
    #     downloadFile = os.path.join(downloadPath, filename)
    #
    #     url = "http://www.westcoast.fisheries.noaa.gov/publications/gis_maps/gis_data/salmon_steelhead/esu/" + filename
    #
    #     arcpy.AddMessage("Downloading " + filename + " to " + downloadPath)
    #
    #     urllib.urlretrieve(url, downloadFile)

    filename = "crithab_all_layers.zip"

    downloadPath = r"C:\Users\jklaus\Documents\Python_Testing\fire_retardant\Downloads\NOAA_ESU"

    downloadFile = os.path.join(downloadPath, filename)

    url = "https://ecos.fws.gov/docs/crithab/crithab_all/" + filename

    arcpy.AddMessage("Downloading " + filename + " to " + downloadPath)

    urllib.urlretrieve(url, downloadFile)


except arcpy.ExecuteError:
    arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
    arcpy.AddMessage(e)