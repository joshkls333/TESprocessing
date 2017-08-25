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

url = "ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Hydrography/NHD/HU4/HighResolution/GDB/"

urllib.urlretrieve(url, "NHD_H_1802_GDB.zip")
