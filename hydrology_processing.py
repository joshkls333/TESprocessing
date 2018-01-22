# ---------------------------------------------------------------------------
# hydrology_processing.py
#
# Description: Pulls three feature classes of data from downloaded Geodatabases on
#              hydrology: NHDArea, NHDFlowline, and NHD Waterbody. This data will be
#              pulled from all the SubRegions covering California. The data is then
#              projected into a GDB as Nad83 CAALB. A select runs on each layer based
#              on FCode or FType. Fields are added and updated with relevant FRA information.
#              All of the feature classes from each SubRegion are merged based on type. Note that the
#              Feature classes for Area and Waterbody and merged together as well.
#              A Buffer analysis runs on each merged feature class of Area, Flowline, and Waterbody.
#              The buffered feature class is then intersected with the Land Ownership feature
#              class to obtain the UnitID. The feature classes are then dissolved to just the
#              relevant FRA fields added earlier.
#
# Arcpy Usage: FeatureClassToShapefile_conversion, Rename_management, Project_management,
#              FeatureClassToGeodatabase_conversion, MakeFeatureLayer_management, SelectLayerByAttribute_management,
#              CopyFeatures_management, GetCount_management, AddField_management, UpdateCursor, Merge_management,
#              Buffer_analysis, RepairGeometery_management, PairwiseIntersect_analysis, PairwiseDissolve_analyis
#
# Runtime Estimates: Total time = 4 hr 21 min 7 sec
#                    Export and projection of original data = 55 min
#
# Created by: Josh Klaus 08/24/2017 jklaus@fs.fed.us
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import sys
import os
import datetime

# Set workspace or obtain from user input
# in_workspace = "C:\\Users\\jklaus\\Documents\\Python_Testing\\fra_new\\"
in_workspace = sys.argv[1]

arcpy.env.workspace = in_workspace
arcpy.env.overwriteOutput = True

# using the now variable to assign year every time there is a hardcoded 2017
now = datetime.datetime.today()
curMonth = str(now.month)
curYear = str(now.year)
arcpy.AddMessage("Year is " + curYear)

# hydroWorkspace = in_workspace + "\\" + "NHD" + curYear + "\\" + "Subregions" + "\\"

hydroWorkspace = in_workspace + "\\" + "Downloads" + "\\" + "Hydro" + "\\"

outputDir = in_workspace + "\\" + "Output"

outputHydroDir = "Hydro" + curYear

outputWorkspace = outputDir + "\\" + outputHydroDir + "\\"

hydroFeatureDataset = "\\" + "Hydrography" + "\\"

# Need to rename when done with testing
projectedGDB = "Hydro_" + curYear + "_CAALB83.gdb"

outputProjGDB = outputWorkspace + projectedGDB

sr = arcpy.SpatialReference(3310)

subRegionList = ["1503", "1604", "1605", "1606", "1710", "1712",
                "1801", "1802", "1803", "1804", "1805", "1806",
                "1807", "1808", "1809", "1810"]

# subRegionList = ["1503", "1801"]

nhdAreaFC = "NHDArea"
nhdFlowlineFC = "NHDFlowline"
nhdWaterbodyFC = "NHDWaterbody"

waterFeatureList = [nhdAreaFC, nhdFlowlineFC, nhdWaterbodyFC]

nhdAreaList = []
nhdFlowlineList = []
nhdWaterbodyList = []

nhdAreaMerge = "NHDArea_Merge"
nhdFlowlineMerge = "NHDFlowline_Merge"
nhdWaterbodyMerge = "NHDWaterBody_Merge"
nhdArea_WaterbodyMerge = "NHDWaterbody_Area_Merge"

mergeList = [nhdAreaMerge, nhdFlowlineMerge, nhdWaterbodyMerge, nhdArea_WaterbodyMerge]

nhdAreaBuffer = "NHDArea_Merge_Buff"
nhdFlowlineBuffer = "NHDFlowline_Merge_Buff"
nhdWaterbodyBuffer = "NHDWaterBody_Merge_Buff"
nhdArea_WaterbodyBuffer = "NHDWaterbody_Area_Merge_Buff"

bufferList = [nhdAreaMerge, nhdFlowlineMerge, nhdWaterbodyMerge, nhdArea_WaterbodyMerge]

intersectList = []

bufferField = "BUFFM_FIRE"

usfsOwnershipFeatureClass = in_workspace + \
                            "\\USFS_Ownership_LSRS\\" + curYear + \
                            "_USFS_Ownership_CAALB83.gdb\\USFS_OwnershipLSRS_" + curYear

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
            arcpy.AddMessage("______________________________________")
            arcpy.AddMessage("Processing " + hydroGDB)

            for waterFeature in waterFeatureList:
                arcpy.AddMessage("--------------------------------------")
                arcpy.AddMessage("processing " + waterFeature)

                flowlineShapefile = waterFeature + ".shp"

                inHydroFD = hydroWorkspace + hydroGDB + hydroFeatureDataset
                inHydroFC = inHydroFD + waterFeature
                arcpy.AddMessage("Origin of Data: " + inHydroFC)

                arcpy.AddMessage("Exporting " + waterFeature + " to shapefile for projecting")
                arcpy.FeatureClassToShapefile_conversion(inHydroFC, outputWorkspace)

                newShapefile = waterFeature + "_" + region

                # Rename files to add Subregion to name to distinguish different feature classes as loop runs
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
                    selectQuery = "( FCode = 46000 OR FCode = 46003 OR FCode = 46006 )"

                arcpy.AddMessage("Selecting features based on following Select Query: " + selectQuery)
                arcpy.MakeFeatureLayer_management(inSelectFC, "lyr" )

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
                    elif fTypefield == 436:
                        row.CMNT_FIRE = "FType 436 - Reservoir"
                        row.INST_FIRE = "Reservoir"
                    elif fTypefield == 466:
                        row.CMNT_FIRE = "FType 466 - Swamp Marsh"
                        row.INST_FIRE = "Swamp Marsh"
                    elif fTypefield == 493:
                        row.CMNT_FIRE = "FType 493 - Estuary"
                        row.INST_FIRE = "Estuary"

                    cur.updateRow(row)

                del cur

                if waterFeature == nhdAreaFC:
                    nhdAreaList.append(selectFC)
                elif waterFeature == nhdFlowlineFC:
                    nhdFlowlineList.append(selectFC)
                elif waterFeature == nhdWaterbodyFC:
                    nhdWaterbodyList.append(selectFC)

        else:
            arcpy.AddMessage(region + " GDB does not exist may need to download and unzip")

    arcpy.AddMessage("________________________________________________")
    arcpy.AddMessage("------------------------------------------------")
    arcpy.AddMessage("________________________________________________")

    arcpy.AddMessage("Merging Flowlines")
    arcpy.Merge_management(nhdFlowlineList, outputProjGDB + "\\" + nhdFlowlineMerge)

    arcpy.AddMessage("Merging Areas")
    arcpy.Merge_management(nhdAreaList, outputProjGDB + "\\" + nhdAreaMerge)

    arcpy.AddMessage("Merging Waterbodies")
    arcpy.Merge_management(nhdWaterbodyList, outputProjGDB + "\\" + nhdWaterbodyMerge)

    arcpy.AddMessage("Merging Areas and Waterbodies")
    arcpy.Merge_management([outputProjGDB + "\\" + nhdAreaMerge, outputProjGDB + "\\" + nhdWaterbodyMerge],
                            outputProjGDB + "\\" + nhdArea_WaterbodyMerge)

    arcpy.AddMessage("__________________________________________________")
    arcpy.AddMessage("--------------------------------------------------")
    arcpy.AddMessage("__________________________________________________")

    for item in mergeList:
        arcpy.AddMessage("|------------------------------------------------|")
        arcpy.AddMessage("|------------------------------------------------|")
        arcpy.AddMessage("__________________________________________________")

        arcpy.AddMessage("Buffering " + item + " features ....")
        bufferInput = outputProjGDB + "\\" + item
        bufferOutput = outputProjGDB + "\\" + item + "_Buff"

        arcpy.Buffer_analysis(bufferInput, bufferOutput, bufferField)

        arcpy.AddMessage("Repairing Geometry of Buffered " + item)
        arcpy.RepairGeometry_management(bufferOutput)

        # usfsOwnershipFeatureClass = in_workspace + \
        #                             "\\USFS_Ownership_LSRS\\2017_USFS_Ownership_CAALB83.gdb\\USFS_OwnershipLSRS_2017"

        intersectFeatureClass = bufferOutput + "_intersect"

        arcpy.AddMessage("Intersecting with USFS Ownership feature class .....")
        arcpy.AddMessage("Please be patient while this runs .....")

        if sys.version_info[0] < 3:
            arcpy.Intersect_analysis([bufferOutput, usfsOwnershipFeatureClass], intersectFeatureClass)
        else:
            arcpy.PairwiseIntersect_analysis([bufferOutput, usfsOwnershipFeatureClass], intersectFeatureClass)

        arcpy.AddMessage("Completed Intersection")

        arcpy.AddMessage(" ____________________________________________________________________")

        arcpy.AddMessage("Updating UnitID field from intersection")

        cur = arcpy.UpdateCursor(intersectFeatureClass)

        field = "UnitID_FS"

        # populating UnitID field with UnitID_FS field
        for row in cur:
            row.UnitID = str(row.getValue(field))
            cur.updateRow(row)

        del cur

        arcpy.AddMessage("Repairing Geometry ......")
        arcpy.RepairGeometry_management(intersectFeatureClass)

        # make a copy of intersectFeatureClass for NOAA processing

        arcpy.AddMessage("Selecting out Intermittents")

        perennialFeatureClass = outputProjGDB + "\\" + item + "_perennial"

        arcpy.MakeFeatureLayer_management(intersectFeatureClass, "lyr")

        if item == "NHDFlowline_Merge":
            arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "(FCode <> 46000) AND (FCode <> 46003)")
            arcpy.AddMessage("Selecting out 46000 and 46003 for Flowlines")
        else:
            arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "(FCode <> 46003)")
            arcpy.AddMessage("Selecting out 46003 for Waterbodies and Areas")

        result = arcpy.GetCount_management("lyr")
        count = int(result.getOutput(0))
        arcpy.AddMessage("Total Number of Records: " + str(count))

        if count > 0:
            arcpy.AddMessage("Copying selected records to Geodatabase without intermittent data.")
            arcpy.CopyFeatures_management("lyr", perennialFeatureClass)

        arcpy.AddMessage("Dissolving Features")

        dissolveFeatureClass = perennialFeatureClass + "_dissolved"

        if sys.version_info[0] < 3:
            arcpy.Dissolve_management(perennialFeatureClass, dissolveFeatureClass,
                                            ["UnitID", "GRANK_FIRE", "SNAME_FIRE", "CNAME_FIRE", "SOURCEFIRE",
                                             "BUFFT_FIRE", "BUFFM_FIRE", "CMNT_FIRE", "INST_FIRE", "BUFF_DIST"], "", "SINGLE_PART")
        else:
            arcpy.PairwiseDissolve_analysis(perennialFeatureClass, dissolveFeatureClass,
                                        ["UnitID", "GRANK_FIRE", "SNAME_FIRE", "CNAME_FIRE", "SOURCEFIRE",
                                         "BUFFT_FIRE", "BUFFM_FIRE", "CMNT_FIRE", "INST_FIRE", "BUFF_DIST"])

        arcpy.AddMessage("Repairing Dissolved Geometry ......")
        arcpy.RepairGeometry_management(dissolveFeatureClass)
        arcpy.AddMessage("Dissolve and Repair complete")
        arcpy.AddMessage(" ____________________________________________________________________")

        interimfc = outputProjGDB + "\\" + item + "_geocomplete"

        arcpy.CopyFeatures_management(dissolveFeatureClass, interimfc)

except arcpy.ExecuteError:
    arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
    arcpy.AddMessage(e)

