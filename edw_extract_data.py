# ---------------------------------------------------------------------------
# edw_extract_data.py
#
# Description: Selects and extracts data from EDW for 4 feature classes:
#              TESP, FishWildlife_Observation, WildlifeSites, BasicOwnership
#              Selects all data for Region 5 with first three and includes TBMU
#              for Ownership feature class. Stores all data in a geodatabase in
#              a folder stored on the workspace provided. Suggest the workspace
#              for the user on the T drive. After that it can be copied to local
#              C drive output directory for usage in next steps. Note the Land
#              Ownership layer uses a dictionary to add the UnitID field and populate
#              it according to the FORESTNAME field.
#
# Runtime Estimates: 17 min 46 sec on Citrix.
#
# Created by: Josh Klaus 08/30/2017 jklaus@fs.fed.us
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import sys
import os
import datetime

# Set workspace or obtain from user input
# in_workspace = "T:\FS\NFS\R05\Program\\6800InformationMgmt\GIS\Workspace\jklaus\\Python\\"
in_workspace = sys.argv[1]

# using the now variable to assign year everytime there is a hardcoded 2017
now = datetime.datetime.today()
curMonth = str(now.month)
curYear = str(now.year)
arcpy.AddMessage("Year is " + curYear)


arcpy.env.workspace = in_workspace
arcpy.env.overwriteOutput = True

edwDataWorkspace = "T:\\FS\\Reference\\GeoTool\\agency\\DatabaseConnection\\edw_sde_default_as_myself.sde"

dataTESP = edwDataWorkspace + "\\S_USA.TESP\\S_USA.TESP_OccurrenceAll"

dataFishWildlifeObs = edwDataWorkspace + "\\S_USA.Fish_and_Wildlife\\S_USA.FishWildlife_Observation"

dataWildlifeSites = edwDataWorkspace + "\\S_USA.Fish_and_Wildlife\\S_USA.WildlifeSites"

dataLandBasic = edwDataWorkspace + "\\S_USA.Land\\S_USA.BasicOwnership"

newPath = in_workspace + "\\" + "EDW_Extract"
edwGDB = "edw_extract.gdb"
selectQuery = "FS_UNIT_ID LIKE '05%'"

landSelectQuery = "((REGION = '05') OR (FORESTNAME = 'Lake Tahoe Basin Management Unit')) " \
                  "AND (OWNERCLASSIFICATION = 'USDA FOREST SERVICE')"

newTESPFeatureClass = "TESP_Extract"
r5TESPFeatureClass = "TESP_region5"

newWildObsFeatureClass = "Wild_Obs_Extract"
r5WildObsFeatureClass = "Wild_Obs_region5"

newWildSitesFeatureClass = "Wild_Sites_Extract"
r5WildSitesFeatureClass = "Wild_Sites_region5"

newLandFeatureClass = "Land_Extract"
r5LandFeatureClass = "Land_region5"

forestGDBDict = {"Angeles National Forest": "0501",
                 "San Bernardino National Forest": "0512",
                 "Cleveland National Forest": "0502",
                 "Eldorado National Forest": "0503",
                 "Inyo National Forest": "0504",
                 "Klamath National Forest": "0505",
                 "Lassen National Forest": "0506",
                 "Los Padres National Forest": "0507",
                 "Modoc National Forest": "0509",
                 "Mendocino National Forest": "0508",
                 "Plumas National Forest": "0511",
                 "Shasta-Trinity National Forest": "0514",
                 "Sierra National Forest": "0515",
                 "Sequoia National Forest": "0513",
                 "Six Rivers National Forest": "0510",
                 "Stanislaus National Forest": "0516",
                 "Lake Tahoe Basin Management Unit": "0519",
                 "Tahoe National Forest": "0517"}


if not os.path.exists(newPath):
    arcpy.AddMessage("Creating directory for EDW Data Extract ....")
    os.makedirs(newPath)
    arcpy.AddMessage("Creating Geodatabase for storing EDW Data Extract ....")
    arcpy.CreateFileGDB_management(newPath, edwGDB)

newWorkSpace = newPath + "\\" + edwGDB + "\\"

edwList = ["TESP", "Wild_Obs", "Wild_Sites", "Land"]

try:
    for edwData in edwList:

        extractWorkSpace = newWorkSpace + "\\" + edwData + "_Extract"
        r5WorkSpace = newWorkSpace + "\\" + edwData + "_region5"

        arcpy.AddMessage("Copying features from EDW to T drive workspace for dataset: " + edwData)
        if edwData == "TESP":
            arcpy.CopyFeatures_management(dataTESP, extractWorkSpace)
        elif edwData == "Wild_Obs":
            arcpy.CopyFeatures_management(dataFishWildlifeObs, extractWorkSpace)
        elif edwData == "Wild_Sites":
            arcpy.CopyFeatures_management(dataWildlifeSites, extractWorkSpace)
        elif edwData == "Land":
            arcpy.CopyFeatures_management(dataLandBasic, extractWorkSpace)

        arcpy.MakeFeatureLayer_management(extractWorkSpace, "lyr" )

        arcpy.AddMessage("Selecting layers based on selection ....")
        if edwData == "Land":
            arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", landSelectQuery)
        else:
            arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", selectQuery )

        arcpy.AddMessage("Selecting feature from Region 5")
        result = arcpy.GetCount_management(extractWorkSpace)
        count = int(result.getOutput(0))
        arcpy.AddMessage("Total Number of Records: " + str(count))

        arcpy.AddMessage("Copying selected records to separate feature class with only Region 5 data")
        arcpy.CopyFeatures_management("lyr", r5WorkSpace)

        if edwData == "Land":
            arcpy.AddMessage("Adding Unit UnitID_FS field")
            arcpy.AddField_management(r5WorkSpace, "UnitID_FS", "TEXT", "", "", "5", "", "NULLABLE",
                                      "NON_REQUIRED", "")

            arcpy.AddMessage("Updating UnitID_FS fields")

            cur = arcpy.UpdateCursor(r5WorkSpace)

            forestField = "FORESTNAME"

            for row in cur:
                row.UnitID_FS = forestGDBDict.get(row.getValue(forestField))

                cur.updateRow(row)

            del cur

            projectedGDB = curYear + "_USFS_Ownership_CAALB83.gdb"
            arcpy.CreateFileGDB_management(newPath, projectedGDB)
            projectedWorkspace = newPath + "\\" + projectedGDB + "\\" + "USFS_OwnershipLSRS_" + curYear

            spatial_ref = arcpy.Describe(r5WorkSpace).spatialReference

            arcpy.AddMessage("Current Spatial Reference is : " + spatial_ref.name)

            sr = arcpy.SpatialReference(3310)

            if spatial_ref.name != "NAD_1983_California_Teale_Albers":
                arcpy.AddMessage("Reprojecting layer to NAD 1983 California Teale Albers ....")
                arcpy.Project_management(r5WorkSpace, projectedWorkspace, sr)

except arcpy.ExecuteError:
    arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
    arcpy.AddMessage(e)
