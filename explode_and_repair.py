
# explode_and_repair.py
#
# Usage: MultipartToSinglepart_management RepairGeometry_management
# Description: Separates Multipart geometry in to single part geometry
#              and reparis any geometry issues
# Created by: Josh Klaus 08/02/2017
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import sys
import csv

in_workspace = r"C:\Users\jklaus\Documents\Python_Testing\fire_retardant\2017_EDW_CAALB83.gdb"
# in_workspace = sys.argv[1]

arcpy.env.workspace = in_workspace
arcpy.env.overwriteOutput = True

intable = r"C:\Users\jklaus\Documents\Python_Testing\fire_retardant\2017_EDW_CAALB83.gdb\EDW_TESP_2017_OccurrenceAll_FoundPlants"
# intable = sys.argv[2]

outtable = intable + "_newJ"

try:


    outFeatureClass = outtable + "_singlepart"

    arcpy.AddMessage("Converting multipart geometry to singlepart .....")

    arcpy.MultipartToSinglepart_management(outtable, outFeatureClass)

    inCount = int(arcpy.GetCount_management(outtable).getOutput(0))
    outCount = int(arcpy.GetCount_management(outFeatureClass).getOutput(0))

    arcpy.AddMessage("Number of new records: " + str(outCount - inCount))

    arcpy.AddMessage("Repairing Geometry ......")
    arcpy.RepairGeometry_management(outFeatureClass)

except arcpy.ExecuteError:
    arcpy.GetMessages()
except Exception as e:
    arcpy.AddMessage(e)
