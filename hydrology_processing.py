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

# Set workspace or obtain from user input
in_workspace = "C:\\Users\\jklaus\\Documents\\Python_Testing\\fire_retardant\\"
# in_workspace = sys.argv[1]

arcpy.env.workspace = in_workspace
arcpy.env.overwriteOutput = True

# using the now variable to assign year everytime there is a hardcoded 2017
now = datetime.datetime.today()
curMonth = str(now.month)
curYear = str(now.year)
arcpy.AddMessage("Year is " + curYear)

hydroWorkspace = in_workspace + "NHD2017" + "\\" + "Subregions" + "\\"

outputDir = in_workspace + "\\" + "Output"

outputHydroDir = "Hydro" + curYear

outputWorkspace = outputDir + "\\" + outputHydroDir + "\\"

hydroFeatureDataset = "\\" + "Hydrography" + "\\"

projectedGDB = "Hydro_Test_2017_CAALB83_newproj.gdb"

outputProjGDB = outputWorkspace + projectedGDB

sr = arcpy.SpatialReference(3310)

subRegionList = ["1503", "1604", "1605", "1606", "1710", "1801",
                 "1802", "1803", "1804", "1805", "1806", "1807",
                 "1808", "1809", "1810"]

nhdAreaFC = "NHDArea"
nhdFlowlineFC = "NHDFlowline"
nhdWaterbodyFC = "NHDWaterbody"

waterFeatureList = [nhdAreaFC, nhdFlowlineFC, nhdWaterbodyFC]

try:

    if not os.path.exists(outputDir):
        arcpy.AddMessage("Creating directory for Output")
        os.makedirs(outputDir)

    if not os.path.exists(outputDir + "\\" + outputHydroDir):
        arcpy.AddMessage("Creating output directory for " + outputHydroDir)
        os.makedirs(outputDir + "\\" + outputHydroDir)

    if arcpy.Exists(outputWorkspace + "\\" + projectedGDB):
        newHydroWorkSpace = outputWorkspace + "\\" + projectedGDB + "\\"
    else:
        arcpy.CreateFileGDB_management(outputWorkspace, projectedGDB)
        newHydroWorkSpace = outputWorkspace + "\\" + projectedGDB + "\\"

    arcpy.AddMessage("Ouput Workspace: " + newHydroWorkSpace)

    for region in subRegionList:
        hydroGDB = "NHD_H_" + region + "_GDB.gdb"

        if arcpy.Exists(hydroWorkspace + hydroGDB):
            arcpy.AddMessage("Processing " + hydroGDB)

            for waterFeature in waterFeatureList:
                arcpy.AddMessage("processing " + waterFeature)

                flowlineShapefile = waterFeature + ".shp"

                inHydroFD = hydroWorkspace + hydroGDB + hydroFeatureDataset
                inHydroFC = inHydroFD + waterFeature
                arcpy.AddMessage("Origin of Data: " + inHydroFC)

                arcpy.AddMessage("Exporting " + waterFeature + " to shapefile for projecting")
                arcpy.FeatureClassToShapefile_conversion(inHydroFC, outputWorkspace)

                newShapefile = waterFeature + "_" + region

                arcpy.Rename_management(outputWorkspace + waterFeature + ".shp", newShapefile)

                inProjShapefile = outputWorkspace + newShapefile + ".shp"
                outProjShapefile = outputWorkspace + newShapefile + "_proj.shp"

                spatial_ref = arcpy.Describe(inProjShapefile).spatialReference

                arcpy.AddMessage("Current Spatial Reference is : " + spatial_ref.name)

                if spatial_ref.name != "NAD_1983_California_Teale_Albers":
                    arcpy.AddMessage("Reprojecting shapefile to NAD 1983 California Teale Albers")
                    arcpy.Project_management(inProjShapefile, outProjShapefile, sr)
                    arcpy.AddMessage("reprojection complete")

                arcpy.AddMessage("Converting shapefile to GDB")
                arcpy.FeatureClassToGeodatabase_conversion(outProjShapefile, newHydroWorkSpace)
                arcpy.AddMessage("Finished converting shapefile to GDB")

                inSelectFC = newHydroWorkSpace + newShapefile + "_proj"
                selectFC = newHydroWorkSpace + newShapefile + "_select"

                selectQuery = ""

                if waterFeature == nhdFlowlineFC:
                    selectQuery = "( FCode = 46000 OR FCode = 46003 OR FCode = 46006 )"
                elif waterFeature == nhdWaterbodyFC:
                    selectQuery = "(  FType = 436 OR FType = 466 OR FType = 493 " \
                                  "OR FCode = 39004 OR FCode = 39009 OR FCode = 39010 OR FCode = 39011)"
                elif waterFeature == nhdAreaFC:
                    selectQuery = "( FCode = 46003 OR FCode = 46006 )"

                arcpy.MakeFeatureLayer_management(inSelectFC, "lyr" )

                arcpy.AddMessage("Selecting records based on selection ..")
                arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", selectQuery )

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
                    fCodefield = row.getValue("FCode")
                    fTypefield = row.getValue("FType")

                    row.SOURCEFIRE = "NHD Subbasins " + curMonth + " " + curYear
                    row.SNAME_FIRE = "Hydro"
                    row.CNAME_FIRE = "Hydro"
                    row.BUFFT_FIRE = "300"
                    row.BUFFM_FIRE = 91.44
                    if waterFeature == nhdAreaFC:
                        row.GRANK_FIRE = "NHDArea Stream/River"
                    elif waterFeature == nhdWaterbodyFC:
                        row.GRANK_FIRE = "NHD Waterbody"
                    elif waterFeature == nhdFlowlineFC:
                        row.GRANK_FIRE = "NHDFlowline Stream/River"

                    if fCodefield == 46000:
                        row.CMNT_FIRE = "FCode 46000 - Stream/River"
                        row.INST_FIRE = "Stream/River"
                    elif fCodefield == 46003:
                        row.CMNT_FIRE = "FCode 46003 - Stream/River Intermittent"
                        row.INST_FIRE = "Stream/River Intermitten"
                    elif fCodefield == 46006:
                        row.CMNT_FIRE = "FCode 46006 - Stream/River Perennial"
                        row.INST_FIRE = "Stream/River Perennial"
                    elif fCodefield == 39004:
                        row.CMNT_FIRE = "FCode 39004 - LakePond Perennial"
                        row.INST_FIRE = "LakePond Perennial"
                    elif fCodefield == 39009:
                        row.CMNT_FIRE = "FCode 39009 - LakePond Perennial Average Stage"
                        row.INST_FIRE = "LakePond Perennial Average Stage"
                    elif fCodefield == 39010:
                        row.CMNT_FIRE = "FCode 39010 - LakePond Perennial Normal Pool"
                        row.INST_FIRE = "LakePond Perennial Normal Pool"
                    elif fCodefield == 39011:
                        row.CMNT_FIRE = "FCode 39011 - LakePond Perennial Date of Photography"
                        row.INST_FIRE = "LakePond Perennial Date of Photography"
                    elif  fTypefield == 436:
                        row.CMNT_FIRE = "FType 436 - Reservoir"
                        row.INST_FIRE = "Reservoir"
                    elif  fTypefield == 466:
                        row.CMNT_FIRE = "FType 466 - Swamp Marsh"
                        row.INST_FIRE = "Swamp Marsh"
                    elif  fTypefield == 493:
                        row.CMNT_FIRE = "FType 493 - Estuary"
                        row.INST_FIRE = "Estuary"

                    cur.updateRow(row)

                del cur


        else:
            arcpy.AddMessage("GDB does not exist may need to download and unzip")

except arcpy.ExecuteError:
    arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
    arcpy.AddMessage(e)

