# noaa_use_processing.py
#
# Description: Used to process all the NOAA ESU layers by clipping to
#               Hydrology layers to prepare for intersection
# Created by: Josh Klaus 08/25/2017 jklaus@fs.fed.us
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import sys
import csv
import os
import datetime
import shutil

# Set workspace or obtain from user input
in_workspace = "C:\\Users\\jklaus\\Documents\\Python_Testing\\fire_retardant\\"
# in_workspace = sys.argv[1]

arcpy.env.workspace = in_workspace
arcpy.env.overwriteOutput = True

# using the now variable to assign year everytime there is a hardcoded 2017
now = datetime.datetime.today()
curYear = str(now.year)
curMonth = now.strftime("%B")
arcpy.AddMessage("Month is " + curMonth)
arcpy.AddMessage("Year is " + curYear)

esuSpeciesList = ["CKCAC", "CKCVF", "CKCVS", "CKSAC",
                  "STCCV", "STNCA", "STSCC", "STSCA", "COSNC"]

# esuSpeciesList = ["COSNC"]

noaaWorkspace = in_workspace + "\\NOAA_ESU\\"
hydroClipWorkspace = in_workspace + "\\NHD2017\\2017_NHDfinal_CAALB83.gdb\\"
# will need to rename these when done testing
flowClipFeatClass = hydroClipWorkspace + "NHD_Flowline_2017"
bodyClipFeatClass = hydroClipWorkspace + "NHDWaterBody_2017"

chinookFolder = noaaWorkspace + "Chinook" + "\\"
cohoFolder = noaaWorkspace + "Coho" + "\\"
steelFolder = noaaWorkspace + "Steelhead" + "\\"

sr = arcpy.SpatialReference(3310)

# inTable = sys.argv[2]

layerType = "NOAA_ESU"

outputDir = in_workspace + "\\" + "Output"
if not os.path.exists(outputDir):
    arcpy.AddMessage("Creating directory for Output")
    os.makedirs(outputDir)

if not os.path.exists(outputDir + "\\" + layerType):
    arcpy.AddMessage("Creating output directory for " + layerType)
    os.makedirs(outputDir + "\\" + layerType)

layerWorkSpace = outputDir + "\\" + layerType + "\\"
projectedGDB = layerType + "_Test_2017_CAALB83_newproj.gdb"

if arcpy.Exists(layerWorkSpace + "\\" + projectedGDB):
    newProjectWorkSpace = layerWorkSpace + "\\" + projectedGDB + "\\"
else:
    arcpy.CreateFileGDB_management(layerWorkSpace, projectedGDB)
    newProjectWorkSpace = layerWorkSpace + "\\" + projectedGDB + "\\"

arcpy.AddMessage("Layer Type: " + layerType)

try:

    for species in esuSpeciesList:
        arcpy.AddMessage("Processing: " + species)
        # need to fix how the original shapefiles arrive in output directory
        if species.startswith("CK"):
            arcpy.CopyFeatures_management(chinookFolder + species + ".shp", layerWorkSpace + species + ".shp")
        elif species.startswith("ST"):
            arcpy.CopyFeatures_management(steelFolder + species + ".shp", layerWorkSpace + species + ".shp")
        elif species.startswith("CO"):
            arcpy.CopyFeatures_management(cohoFolder + species + ".shp", layerWorkSpace + species + ".shp")
        inProjShapefile = layerWorkSpace + species + ".shp"
        outProjShapefile = layerWorkSpace + species + "_proj.shp"

        spatial_ref = arcpy.Describe(inProjShapefile).spatialReference

        arcpy.AddMessage("Current Spatial Reference is : " + spatial_ref.name)

        if spatial_ref.name != "NAD_1983_California_Teale_Albers":
            arcpy.AddMessage("Reprojecting shapefile to NAD 1983 California Teale Albers")
            arcpy.Project_management(inProjShapefile, outProjShapefile, sr)
            arcpy.AddMessage("reprojection complete")

        arcpy.AddMessage("Converting shapefile to GDB")
        arcpy.FeatureClassToGeodatabase_conversion(outProjShapefile, newProjectWorkSpace)
        arcpy.AddMessage("Finished converting shapefile to GDB")

        inSelectFC = newProjectWorkSpace + species + "_proj"
        selectFC = newProjectWorkSpace + species + "_select"

        selectQuery = "( Class = 'Accessible' )"

        arcpy.MakeFeatureLayer_management(inSelectFC, "lyr")

        arcpy.AddMessage("Selecting records based on selection where [Class = 'Accessible'] ")
        arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", selectQuery)

        arcpy.AddMessage("Copying selected records to new feature ......")
        arcpy.CopyFeatures_management("lyr", selectFC)

        result = arcpy.GetCount_management(selectFC)
        count = int(result.getOutput(0))
        arcpy.AddMessage("Total Number of Records: " + str(count))

        arcpy.AddMessage("Adding fields")

        arcpy.AddField_management(selectFC, "UnitID", "TEXT", "", "", "5", "", "NULLABLE",
                                  "NON_REQUIRED", "")
        arcpy.AddField_management(selectFC, "GRANK_FIRE", "TEXT", "", "", "50", "", "NULLABLE",
                                  "NON_REQUIRED", "")
        arcpy.AddField_management(selectFC, "SOURCEFIRE", "TEXT", "", "", "50", "", "NULLABLE",
                                  "NON_REQUIRED", "")
        arcpy.AddField_management(selectFC, "SNAME_FIRE", "TEXT", "", "", "60", "", "NULLABLE",
                                  "NON_REQUIRED", "")
        arcpy.AddField_management(selectFC, "CNAME_FIRE", "TEXT", "", "", "60", "", "NULLABLE",
                                  "NON_REQUIRED", "")
        arcpy.AddField_management(selectFC, "BUFFT_FIRE", "SHORT", "", "", "", "", "NULLABLE",
                                  "NON_REQUIRED", "")
        arcpy.AddField_management(selectFC, "BUFFM_FIRE", "SHORT", "", "", "", "", "NULLABLE",
                                  "NON_REQUIRED", "")
        arcpy.AddField_management(selectFC, "CMNT_FIRE", "TEXT", "", "", "150", "", "NULLABLE",
                                  "NON_REQUIRED", "")
        arcpy.AddField_management(selectFC, "INST_FIRE", "TEXT", "", "", "150", "", "NULLABLE",
                                  "NON_REQUIRED", "")

        arcpy.AddMessage("Updating fields")

        cur = arcpy.UpdateCursor(selectFC)

        for row in cur:
            row.SOURCEFIRE = "NHD Subbasins " + curMonth + " " + curYear + " within ESU"
            # Need to fix the following - possibly use a dictionary
            row.SNAME_FIRE = species
            row.CNAME_FIRE = species
            row.CMNT_FIRE = "NHD Flowlines and Waterbodies used within accessible ESU"
            row.BUFFT_FIRE = "300"
            row.BUFFM_FIRE = 91.44

            cur.updateRow(row)

        del cur

        arcpy.AddMessage("Clipping to Flowline data")
        outFlowClipFC = selectFC + "_Flowline"
        arcpy.Clip_analysis(selectFC, flowClipFeatClass, outFlowClipFC)

        arcpy.AddMessage("Clipping to Waterbody data")
        outBodyClipFC = selectFC + "_Waterbody"
        arcpy.Clip_analysis(selectFC, bodyClipFeatClass, outBodyClipFC)

        arcpy.AddMessage("Merging both clipped Feature classes")
        mergeFC = selectFC + "_AllHydro"
        arcpy.Merge_management([outFlowClipFC, outBodyClipFC], mergeFC)

        singlePartFeatureClass = mergeFC + "_singlepart"

        arcpy.AddMessage("Converting multipart geometry to singlepart ")

        arcpy.MultipartToSinglepart_management(mergeFC, singlePartFeatureClass)

        inCount = int(arcpy.GetCount_management(mergeFC).getOutput(0))
        outCount = int(arcpy.GetCount_management(singlePartFeatureClass).getOutput(0))

        arcpy.AddMessage("Number of new records: " + str(outCount - inCount))

        arcpy.AddMessage("Repairing Geometry ......")
        arcpy.RepairGeometry_management(singlePartFeatureClass)
        arcpy.AddMessage("Finished with Explode and Repair")


except arcpy.ExecuteError:
    arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
    arcpy.AddMessage(e)