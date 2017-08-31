# select_tes_layer.py
#
# Description: Using original data it projects data to an output geodatabase in
#              Nad83 CAALB projection. The projected data runs through a
#              select based on Scientific Names equal to TES list.
#              This list is referenced by using a csv with Buffers, Common Names,
#              and forest dependent distinctions. FRA specific fields are added
#              to the subset of data. From that relationship a correct
#              buffer value is assigned to populate the buffer field. Before any
#              analysis the data is exported to a geodatabase for the FWS.
#              After the export a buffer analysis runs on certain datasets.
#              This step has several distinct approaches based on what dataset
#              is processing. After this and explode and repair occurs.
#              Certain datasets will require a final merge with special feature classes.
#
# Runtime Estimates:
#
# Created by: Josh Klaus 07/27/2017 jklaus@fs.fed.us
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import sys
import csv
import os
import datetime

# Set workspace or obtain from user input
in_workspace = "C:\\Users\\jklaus\\Documents\\Python_Testing\\fire_retardant\\"
# in_workspace = sys.argv[1]

arcpy.env.workspace = in_workspace
arcpy.env.overwriteOutput = True

# -------------------------------------------------------------------------------
# the following section will create folders and geodatabases to store Deliverables
# for different stages of the processing of the individual databases
# -------------------------------------------------------------------------------

# using the now variable to assign year everytime there is a hardcoded 2017
now = datetime.datetime.today()
curYear = str(now.year)
arcpy.AddMessage("Year is " + curYear)

sciNameField = ""
commonNameField = ""
sourceField = ""

tesvariablelist = ["Endangered", "Threatened", "Sensitive"]

for tes in tesvariablelist:
    newPath = in_workspace + "\\2017_" + tes
    tesGDB = "2017_FRA_" + tes + "_OriginalDataNoBuffers_FWSDeliverable_CAALB83.gdb"

    if not os.path.exists(newPath):
        arcpy.AddMessage("Creating directory for "+ tes + " Data Deliverables ....")
        os.makedirs(newPath)
        arcpy.AddMessage("Creating Geodatabase for " + tes + " Data Deliverables ....")
        arcpy.CreateFileGDB_management(newPath, tesGDB)

# --------------------------------------------------------------------------------
#  Please note the following selections of inTable and csv are file dependent
# --------------------------------------------------------------------------------

layerType = sys.argv[4]

# layerType = "CNDDB"

outputDir = in_workspace + "\\" + "Output"
if not os.path.exists(outputDir):
    arcpy.AddMessage("Creating directory for Output")
    os.makedirs(outputDir)

if not os.path.exists(outputDir + "\\" + layerType):
    arcpy.AddMessage("Creating output directory for " + layerType)
    os.makedirs(outputDir + "\\" + layerType)

layerWorkSpace = outputDir + "\\" + layerType + "\\"
projectedGDB = layerType + "_Test_2017_CAALB83_newproj.gdb"
foundFC = layerType + "_" + curYear + "_original"

arcpy.AddMessage("Layer Type: " + layerType)

#-------------------------------------------------------------------------------------------
# the below is hardcoded values used for testing and debugging
inTable = in_workspace

# inTable = sys.argv[2]

# if inTable == "#":
if layerType == "TESP":
    inTable += "\\USFS_EDW\\EDW_TESP_r05_021617_Everything.gdb\\TESP\\TESP_OccurrenceAll"
elif layerType == "Wildlife_Sites":
    inTable += "\\USFS_EDW\\EDW_FishWildlife_R05_021617_Everything.gdb\\Fish_and_Wildlife\\WildlifeSites"
elif layerType == "Wildlife_Observations":
    inTable += "\\USFS_EDW\\EDW_FishWildlife_R05_021617_Everything.gdb\\Fish_and_Wildlife\\FishWildlife_Observation"
elif layerType == "Critical_Habitat_Lines":
    inTable += "\\CHab\\crithab_all_layers\\CRITHAB_LINE.shp"
elif layerType == "Critical_Habitat_Polygons":
    inTable += "\\CHab\\crithab_all_layers\\CRITHAB_POLY.shp"
elif layerType == "CNDDB":
    inTable += "\\CNDDB\\gis_gov\\cnddb.shp"

#------------------------------------------------------------------------------
# Testing to see if data is projected in NAD 1983 California Teale Albers
# If not run Project_management to project the data
#------------------------------------------------------------------------------

if arcpy.Exists(layerWorkSpace + "\\" + projectedGDB):
    newProjectWorkSpace = layerWorkSpace + "\\" + projectedGDB + "\\" + foundFC
else:
    arcpy.CreateFileGDB_management(layerWorkSpace, projectedGDB)
    newProjectWorkSpace = layerWorkSpace + "\\" + projectedGDB + "\\" + foundFC

selectFC = newProjectWorkSpace + "_select"

arcpy.AddMessage("Origin of Data: " + inTable)

spatial_ref = arcpy.Describe(inTable).spatialReference

arcpy.AddMessage("Current Spatial Reference is : " + spatial_ref.name)

sr = arcpy.SpatialReference(3310)

if spatial_ref.name != "NAD_1983_California_Teale_Albers":
    arcpy.AddMessage("Reprojecting layer to NAD 1983 California Teale Albers ....")
    arcpy.Project_management(inTable, newProjectWorkSpace, sr)

# ------------------------------------------------------------------------------------------
# Adding fields to store information that will be used for final deliverables
# ------------------------------------------------------------------------------------------

arcpy.AddMessage("Adding fields [UnitID, GRANK_FIRE, SOURCEFIRE, SNAME_FIRE, CNAME_FIRE]")
arcpy.AddMessage("Adding fields [BUFFT_FIRE, BUFFM_FIRE, CMNT_FIRE, INST_FIRE]")
if layerType == "CNDDB":
    arcpy.AddMessage("Adding field Type to record Plant vs Animal to filter later after intersection for removal of BDF")

arcpy.AddField_management(newProjectWorkSpace, "UnitID", "TEXT", "", "", "5", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(newProjectWorkSpace, "GRANK_FIRE", "TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(newProjectWorkSpace, "SOURCEFIRE", "TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(newProjectWorkSpace, "SNAME_FIRE", "TEXT", "", "", "60", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(newProjectWorkSpace, "CNAME_FIRE", "TEXT", "", "", "60", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(newProjectWorkSpace, "BUFFT_FIRE", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(newProjectWorkSpace, "BUFFM_FIRE", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(newProjectWorkSpace, "CMNT_FIRE", "TEXT", "", "", "150", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(newProjectWorkSpace, "INST_FIRE", "TEXT", "", "", "150", "", "NULLABLE", "NON_REQUIRED", "")
if layerType == "CNDDB":
    arcpy.AddField_management(newProjectWorkSpace, "Type", "TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")

# Note the different ways of bringing in a csv for lookup data on the buffer amount, forest, and status
# _____________________________________________________________________________________________________

# csvFile = sys.argv[3]

csvFile = in_workspace + "\\csv_tables"

if layerType == "TESP":
    csvFile += "\\TESP_SummaryTable.csv"
elif layerType == "Wildlife_Sites":
    csvFile += "\\Wildlife_Sites_SummaryTable.csv"
elif layerType == "Wildlife_Observations":
    csvFile += "\\Wildlife_Observations_SummaryTable.csv"
elif layerType == "Critical_Habitat_Polygons":
    csvFile += "\\crithab.csv"
elif layerType == "Critical_Habitat_Lines":
    csvFile += "\\crithab.csv"
elif layerType == "CNDDB":
    csvFile += "\\CNDDB_SummaryTable.csv"

arcpy.AddMessage("csv File: " + csvFile)

# uncomment when using arcgis 10.3
with open(csvFile, 'rb') as f:
    reader = csv.reader(f)
    selectionList = list(reader)

# use when using arcgis pro
# with open(csvFile) as f:
#     reader = csv.reader(f)
#     selectionList = list(reader)

arcpy.AddMessage("Listing of csv table data: ")
for item in selectionList:
    arcpy.AddMessage("  " + str(item))

if layerType == "TESP":
    sciNameField = "SCIENTIFIC_NAME"
    commonNameField = "ACCEPTED_COMMON_NAME"
    sourceField = "EDW TESP OccurrencesALL_FoundPlant pulled 2/2017"
elif layerType == "Wildlife_Sites":
    sciNameField = "SCI_NAME"
    commonNameField = "COMMON_NAME"
    sourceField = "EDW Wildlife Sites pulled 2/2017"
elif layerType == "Wildlife_Observations":
    sciNameField = "SCIENTIFIC_NAME"
    commonNameField = "COMMON_NAME"
    sourceField = "EDW OBS FishWildlife pulled 2/2017"
elif layerType == "Critical_Habitat_Polygons":
    sciNameField = "sciname"
    commonNameField = "comname"
    sourceField = "FWS Critical Habitat pulled 2/2017"
elif layerType == "Critical_Habitat_Lines":
    sciNameField = "sciname"
    commonNameField = "comname"
    sourceField = "FWS Critical Habitat pulled 2/2017"
elif layerType == "CNDDB":
    sciNameField = "SNAME"
    commonNameField = "CNAME"
    sourceField = 'CA CNDDB GOV version pulled 2/2017'

# --------------------------------------------------------------------
# Builds the selection query used in SelectLayerByAttribute_management
# customized based on what the Scientific name field is and what other
# specifics we need to filter the data on based on the type of database
# --------------------------------------------------------------------
selectQuery = "(" + sciNameField + " = "

selectionListLength = len(selectionList)

for n in range(1, selectionListLength-1):
    selectQuery += "'" + selectionList[n][0] + "' OR " + sciNameField + " = "

selectQuery += "'" + selectionList[selectionListLength-1][0] + "')"

if layerType == "CNDDB":
    selectQuery += """
                   AND (PRESENCE = 'Presumed Extant') 
                   AND (ACCURACY = '1/10 mile' OR ACCURACY = '1/5 mile' 
                     OR ACCURACY = '80 meters' OR ACCURACY = 'specific area')
                   """
elif layerType == "Wildlife_Sites":
    selectQuery += " AND (ASSOC_OBS > 0) AND (SITE_NAME NOT LIKE '%Study%') "
elif layerType == "Wildlife_Observations":
    selectQuery += " AND (TOTAL_DETECTED > 0 OR TOTAL_DETECTED IS NULL )"
elif layerType == "Critical_Habitat_Lines":
    selectQuery += " OR sciname = 'Oncorhynchus (=Salmo) mykiss' OR sciname = 'Catostomus microps'"
elif layerType == "TESP":
    for n in range(1, selectionListLength-1):
        selectQuery += " OR (ACCEPTED_SCIENTIFIC_NAME = " + "'" + selectionList[n][0] + "')"
        selectQuery += " AND (PLANT_FOUND = 'YES') "

    # Old Hardcoded values for ACCEPTED_SCIENTIFIC_NAME
    # Stacey decided to pull all - which found other hits but not in relevant forests

    # selectQuery += """
    #                 OR ACCEPTED_SCIENTIFIC_NAME = 'Mahonia nevinii'
    #                 OR ACCEPTED_SCIENTIFIC_NAME = 'Stanfordia californica'
    #                 OR ACCEPTED_SCIENTIFIC_NAME = 'Clarkia springvillensis'
    #                 OR ACCEPTED_SCIENTIFIC_NAME = 'Abronia alpina'
    #                 OR ACCEPTED_SCIENTIFIC_NAME = 'Calochortus persistens'
    #                 """

arcpy.AddMessage("The Selection Query will be : " + selectQuery)

# Need to clean this up so select query can be viewed:
# sqLength = int(len(selectQuery))
# n = int(round(len(selectQuery) / 100))
#
# arcpy.AddMessage("The Selection Query will be : " )
# arcpy.AddMessage("  " + selectQuery[0:n])
# arcpy.AddMessage("  " + selectQuery[n:n+100])
# arcpy.AddMessage("  " + selectQuery[n+100:n+200])
# arcpy.AddMessage("  " + selectQuery[n+200:n+300])
# arcpy.AddMessage("  " + selectQuery[n+300:n+400])
# arcpy.AddMessage("  " + selectQuery[n+400:n+800])
# arcpy.AddMessage("  " + selectQuery[n+800:sqLength-100])
# arcpy.AddMessage("  " + selectQuery[n+800:sqLength-100])
# arcpy.AddMessage("  " + selectQuery[sqLength-100:sqLength])

# -----------------------------------------------------------------------------------------

try:

    arcpy.MakeFeatureLayer_management(newProjectWorkSpace, "lyr" )

    arcpy.AddMessage("Selecting layers based on selection ....")
    arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", selectQuery )

    arcpy.AddMessage("Copying selected records to new feature ......")
    arcpy.CopyFeatures_management("lyr", selectFC)

    result = arcpy.GetCount_management(selectFC)
    count = int(result.getOutput(0))
    arcpy.AddMessage("Total Number of Records: " + str(count))

    threatNum = 0
    sensitiveNum = 0
    endangerNum = 0
    otherNum = 0
    arcpy.AddMessage("Populating attributes .....")

    if layerType == "Critical_Habitat_Polygons" or layerType == "Critical_Habitat_Lines":
        cur = arcpy.UpdateCursor(selectFC)

        for row in cur:
            speciesrow = row.getValue(sciNameField)
            bufferAmount = 0

            row.SOURCEFIRE = sourceField
            row.SNAME_FIRE = speciesrow
            row.CNAME_FIRE = row.getValue(commonNameField)
            row.BUFFT_FIRE = bufferAmount
            row.BUFFM_FIRE = bufferAmount * 0.3048

            for item in selectionList:
                if item[0].startswith(speciesrow):
                    row.GRANK_FIRE = item[1]
                    if item[1] == "Threatened":
                        threatNum += 1
                    elif item[1] == "Sensitive":
                        sensitiveNum += 1
                    elif item[1] == "Endangered":
                        endangerNum += 1
                    else:
                        otherNum += 1

            cur.updateRow(row)

        del cur

    elif layerType == "CNDDB":
        cur = arcpy.UpdateCursor(selectFC)
        accuracyField = "ACCURACY"

        for row in cur:
            speciesrow = row.getValue(sciNameField)
            bufferAmount = 0
            accuracy = row.getValue(accuracyField)

            row.SOURCEFIRE = sourceField
            row.SNAME_FIRE = speciesrow
            row.CNAME_FIRE = row.getValue(commonNameField)

            for item in selectionList:

                if item[0].startswith(speciesrow):
                    row.GRANK_FIRE = item[1]
                    row.TYPE = item[5]

                    if accuracy == "1/10 mile":
                        if item[2] == "300":
                            bufferAmount = 3
                        elif item[2] == "600":
                            bufferAmount = 72
                    elif accuracy == "1/5 mile":
                        if item[2] == "300":
                            bufferAmount = 3
                        elif item[2] == "600":
                            bufferAmount = 3
                    elif accuracy == "80 meters":
                        if item[2] == "300":
                            bufferAmount = 38
                        elif item[2] == "600":
                            bufferAmount = 338
                    elif accuracy == "specific area":
                        bufferAmount = int(item[2])
                    else:
                        bufferAmount = 2

            row.BUFFT_FIRE = bufferAmount
            row.BUFFM_FIRE = bufferAmount * 0.3048
            if row.GRANK_FIRE == "Threatened":
                threatNum += 1
            elif row.GRANK_FIRE == "Sensitive":
                sensitiveNum += 1
            elif row.GRANK_FIRE == "Endangered":
                endangerNum += 1
            else:
                otherNum += 1

            cur.updateRow(row)

        del cur

    else:

        forestField = "FS_UNIT_NAME"
        cur = arcpy.UpdateCursor(selectFC)

        for row in cur:
            speciesrow = row.getValue(sciNameField)
            forestrow  = row.getValue(forestField)
            bufferAmount = 1

            row.SOURCEFIRE = sourceField
            row.SNAME_FIRE = speciesrow
            row.CNAME_FIRE = row.getValue(commonNameField)

            for item in selectionList:

                if item[0].startswith(speciesrow) and item[3] == "":
                    row.GRANK_FIRE = item[1]
                    bufferAmount = int(item[2])
                    break

                elif item[0].startswith(speciesrow)  and item[3] == forestrow:
                    row.GRANK_FIRE = item[1]
                    bufferAmount = int(item[2])
                    break

                elif item[0].startswith(speciesrow) and item[3] != forestrow:
                    row.GRANK_FIRE = item[1]
                    bufferAmount = 0

            row.BUFFT_FIRE = bufferAmount
            row.BUFFM_FIRE = bufferAmount * 0.3048

            if row.GRANK_FIRE == "Threatened":
                threatNum += 1
            elif row.GRANK_FIRE == "Sensitive":
                sensitiveNum += 1
            elif row.GRANK_FIRE == "Endangered":
                endangerNum += 1
            else:
                otherNum += 1

            cur.updateRow(row)

        del cur

    arcpy.AddMessage("Number of Endangered = " + str(endangerNum))
    arcpy.AddMessage("Number of Threatened = " + str(threatNum))
    arcpy.AddMessage("Number of Sensitive = " + str(sensitiveNum))
    arcpy.AddMessage("Number of Other = " + str(otherNum))

    arcpy.AddMessage("Splitting current state of data into deliverable Geodatabases .....")

#    does not work in ArcGIS only ArcGIS Pro
#    arcpy.SplitByAttributes_analysis(selectFC, sensitive_gdb, "GRANK_FIRE")

    tesRankList = ["Endangered", "Threatened", "Sensitive"]

    for tesRank in tesRankList:
        arcpy.MakeFeatureLayer_management(selectFC, "lyr")

        arcpy.AddMessage("Selecting records based on " + tesRank + " rank ....")
        arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "GRANK_FIRE = '" + tesRank + "'")

        outlocation = in_workspace + "\\2017_" + tesRank + "\\" + "2017_FRA_" + \
                      tesRank + "_OriginalDataNoBuffers_FWSDeliverable_CAALB83.gdb" + "\\"

        if layerType == "TESP":
            outlocation += "EDW_TESP_2017_" + tesRank + "_OccurrenceAll_FoundPlants_nobuf"
        elif layerType == "Wildlife_Sites":
            outlocation += "EDW_WildlifeSites_2017_" + tesRank + "_nobuf"
        elif layerType == "Wildlife_Observations":
            outlocation += "EDW_FishWildlife_Observation_2017_" + tesRank + "_nobuf"
        elif layerType == "Critical_Habitat_Polygons":
            outlocation += "CHabPolyAllSelectedSpecies_2017_" + tesRank + "_nobuf"
        elif layerType == "Critical_Habitat_Lines":
            outlocation += "CHabLineAllSelectedSpecies_2017_" + tesRank + "_nobuf"
        elif layerType == "CNDDB":
            outlocation += "CNDDB_selects_2017_" + tesRank + "_nobuf"

        result = arcpy.GetCount_management("lyr")
        count = int(result.getOutput(0))
        arcpy.AddMessage("Total Number of Records: " + str(count))

        if count > 0:
            arcpy.AddMessage("Copying selected records to " + tesRank + " Geodatabase ......")
            arcpy.CopyFeatures_management("lyr", outlocation)

# ----------------------------------------------------------------------

    singlePartFeatureClass = newProjectWorkSpace + "_singlepart"
    bufferFC = newProjectWorkSpace + "_buffer"
    singlePartBufferedFC = newProjectWorkSpace + "_buffered_single"
    projGDB = layerWorkSpace + "\\" + projectedGDB + "\\"
    siteMerge = newProjectWorkSpace + "_merge"

    arcpy.AddMessage("Converting multipart geometry to singlepart .....")

    arcpy.MultipartToSinglepart_management(selectFC, singlePartFeatureClass)

    inCount = int(arcpy.GetCount_management(selectFC).getOutput(0))
    outCount = int(arcpy.GetCount_management(singlePartFeatureClass).getOutput(0))

    arcpy.AddMessage("Number of new records: " + str(outCount - inCount))

    arcpy.AddMessage("Repairing Geometry ......")
    arcpy.RepairGeometry_management(singlePartFeatureClass)

    if layerType != "Critical_Habitat_Polygons" and layerType != "Critical_Habitat_Lines":
        arcpy.AddMessage("Buffering features ....")
        bufferField = "BUFFM_FIRE"
        arcpy.Buffer_analysis(singlePartFeatureClass, bufferFC, bufferField)

        arcpy.AddMessage("Converting buffer layer from multipart geometry to singlepart .....")

        arcpy.MultipartToSinglepart_management(bufferFC, singlePartBufferedFC)

        inCount = int(arcpy.GetCount_management(bufferFC).getOutput(0))
        outCount = int(arcpy.GetCount_management(singlePartBufferedFC).getOutput(0))

        arcpy.AddMessage("Number of new records: " + str(outCount - inCount))

        arcpy.AddMessage("Repairing Geometry of singlepart buffer layer ......")
        arcpy.RepairGeometry_management(singlePartBufferedFC)

    if layerType == "CNDDB":

        arcpy.AddMessage("Moving Shasta Crayfish files into Geodatabase")
        # May need to change where this is being pulled
        tempWorkSpace = in_workspace + "\\CNDDB\\2017_CNDDB_CAALB83.gdb\\"
        crayFlowLines = tempWorkSpace + "CNDDB_Endangered_ShastaCrayfish_NHDFlowlines"
        crayWaterBodies = tempWorkSpace + "CNDDB_Endangered_ShastaCrayfish_NHDWaterbodies"
        arcpy.FeatureClassToGeodatabase_conversion([crayFlowLines, crayWaterBodies], projGDB)

        arcpy.AddMessage("Merging the CNDDDB feature class with the Shasta Crayfish files")
        arcpy.Merge_management([crayFlowLines, crayWaterBodies, singlePartBufferedFC], siteMerge)
        arcpy.AddMessage("Finished with merge")

        arcpy.AddMessage("Repairing Geometry of merged layer")
        arcpy.RepairGeometry_management(singlePartBufferedFC)

    elif layerType == "Wildlife_Observations":

        arcpy.AddMessage("Breaking up into three layers prior to intersect")
        arcpy.MakeFeatureLayer_management(singlePartBufferedFC, "lyr")

        tesRankList = ["Endangered", "Threatened", "Sensitive"]

        for tesRank in tesRankList:
            finalWorkSpace = layerWorkSpace + "\\" + projectedGDB + "\\" + \
                             "EDW_FishWildlife_Observation_2017_" + tesRank[:1]

            arcpy.AddMessage("Selecting records based on " + tesRank + " rank ....")
            arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "GRANK_FIRE = '" + tesRank +"'")
            arcpy.AddMessage("Copying selected records to " + tesRank + " Feature Class ......")
            arcpy.CopyFeatures_management("lyr", finalWorkSpace)

    elif layerType == "Wildlife_Sites":
        arcpy.AddMessage("Moving two MYLF study area files into Geodatabase")
        # May need to fix where this data is being pulled
        tmpWorkSpace = in_workspace + "\\USFS_EDW\\2017_EDW_CAALB83.gdb\\"
        studyFlowLines = tmpWorkSpace + "EDW_WildlifeSites_FRASelectionSet_CAALB_NHDFlowlines_MYLF_E_INFStudyAreas_buffered"
        studyWaterBodies = tmpWorkSpace + "EDW_WildlifeSites_FRASelectionSet_CAALB_NHDWaterbodys_MYLF_E_INFStudyAreas_buffered"
        arcpy.FeatureClassToGeodatabase_conversion([studyFlowLines, studyWaterBodies], projGDB)

        arcpy.AddMessage("Merging the Wildlife Sites feature class with the two MYLF study area")
        arcpy.Merge_management([studyFlowLines, studyWaterBodies, singlePartBufferedFC], siteMerge)
        arcpy.AddMessage("Finished with merge")

        arcpy.AddMessage("Repairing Geometry of merged layer")
        arcpy.RepairGeometry_management(singlePartBufferedFC)

    arcpy.AddMessage("Script complete ... check data and make changes ... then proceed to intersection")

    # -----------------------------------------------------------------------------------
    #  Note this process will be run in another script within an
    #  ArcGIS Pro environment using PairwiseIntersect_analysis
    # -----------------------------------------------------------------------------------
    # arcpy.Intersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)
    # arcpy.PairwiseIntersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)

except arcpy.ExecuteError:
    arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
    arcpy.AddMessage(e)

  # Figure out a way to merge the Above section of Code with the Below section of Code

    # ===============================================================
    # ===============================================================
    # ===============================================================
    # ===============================================================


# nameOfFile = sys.argv[3]

local_gdb = in_workspace + "\\Local_Data\\2017_Local_CAALB83.gdb\\"
local_data = local_gdb + "\\Explode"


sr = arcpy.SpatialReference(3310)

if layerType == "Local":
    arcpy.env.workspace = local_data
    if arcpy.Exists(local_gdb + "\\Intersect_New"):
        intersectFeatureDataset = local_gdb + "\\Intersect_New\\"
    else:
        arcpy.CreateFeatureDataset_management(local_gdb, "Intersect_New", 3310)
        intersectFeatureDataset = local_gdb + "\\Intersect_New\\"
elif layerType == "NOAA_ESU":
    noaaGdb = in_workspace + "NOAA_ESU\\2017_NOAA_ESU_CAALB83.gdb"
    arcpy.env.workspace = noaaGdb
    outFeatClass = noaaGdb
else:
    arcpy.env.workspace = in_workspace

arcpy.env.overwriteOutput = True

# The following is used for testing locally. DELETE when done testing.
# outFeatClass = in_workspace + "\\" + layerType + "\\Critical_Habitat_Polygons_Test_2017_CAALB83_newproj.gdb\Critical_Habitat_Polygons_2017_Occurrence_found_newE_singlepart"

# outFeatClass = in_workspace + "\\" + "Output" + "\\" + layerType + "\\TESP_Test_2017_CAALB83_newproj.gdb\\TESP_2017_original_buffered_single"

# outFeatClass = in_workspace + "\\" + layerType + "\\Wildlife_Sites_Test_2017_CAALB83_newproj.gdb\\Wildlife_Sites_2017_Occurrence_found_newE_singlepart_buffer_spart"

outFeatClass = in_workspace + "\\CondorData_noFOIAnoRelease\\2017_Condor_CAALB83.gdb\\CondorHacking_2015"


# outFeatClass = sys.argv[1]

nameOfFile = outFeatClass

nameOfFile = nameOfFile.replace('C:\\Users\\jklaus\\Documents\\Python_Testing\\fire_retardant\\NOAA_ESU\\2017_NOAA_ESU_CAALB83.gdb\\','')
arcpy.AddMessage(nameOfFile)

tesvariablelist = ["Endangered", "Threatened", "Sensitive"]

for tes in tesvariablelist:

    newPath = in_workspace + "2017_" + tes

    # Geodatabases for final merge
    identInterGdb = "2017_" + tes + "_IdentInter_CAALB83.gdb"

    # Geodatabases for FWS Deliverable
    fraDeliverableGdb = "2017_FRA_" + tes + "_OriginalDataBufferedAndNonBufferedAreas_CAALB83.gdb"

    if arcpy.Exists( newPath + "\\" + identInterGdb):
        arcpy.AddMessage(tes + " GDB exists")
    else:
        arcpy.AddMessage("Creating Geodatabase for " + tes + " Data Deliverables containing intersection data ....")
        arcpy.CreateFileGDB_management(newPath, identInterGdb)
        arcpy.CreateFileGDB_management(newPath, fraDeliverableGdb)


def get_filename(tes_rank, orig_filename):

    filename = ""
    if layerType == "TESP":
        filename = "EDW_TESP_2017_OccurrenceAll_FoundPlants_ident_" + tes_rank
    elif layerType == "Wildlife_Sites":
        filename = "EDW_WildlifeSites_2017_ident_" + tes_rank
    elif layerType == "Wildlife_Observations":
        filename = "EDW_FishWildlife_Observation_2017_" + tes_rank[:1] + "_ident"
    elif layerType == "Critical_Habitat_Polygons":
        filename = "CHabPolyAllSelectedSpecies_2017_nobuf_Ident_" + tes_rank
    elif layerType == "Critical_Habitat_Lines":
        filename = "CHabLineAllSelectedSpecies_2017_nobuf_Ident_" + tes_rank
    elif layerType == "CNDDB":
        filename = "CNDDB_2017_All_selectsAndShastaCrayfish_Ident_noBDF_" + tes_rank
    elif layerType == "Condor_Hacking":
        filename = "CNH_2017_ident"
    elif layerType == "Condor_Nest":
        filename = "CN_2017_ident"
    elif layerType == "Local" or layerType == "NOAA_ESU":
        filename = fc

    return filename


def copy_to_gdb(stage, filename):

    for tes_rank in tesvariablelist:
        arcpy.AddMessage(" --------------------------------------------------------------- ")

        arcpy.MakeFeatureLayer_management(filename, "tmplyr")

        arcpy.AddMessage("Selecting records based on " + tes_rank + " rank ....")
        arcpy.SelectLayerByAttribute_management("tmplyr", "NEW_SELECTION", "GRANK_FIRE = '" + tes_rank + "'")

        if stage == "Interim":
            outlocation = in_workspace + "2017_" + tes_rank + "\\" + "2017_FRA_" + \
                          tes_rank + "_OriginalDataBufferedAndNonBufferedAreas_CAALB83.gdb" + "\\"
        else:
            outlocation = in_workspace + "2017_" + tes_rank + "\\2017_" + tes_rank + "_IdentInter_CAALB83.gdb\\"

        outputfilename = get_filename(tes_rank, filename)

        outlocation += outputfilename

        result = arcpy.GetCount_management("tmplyr")
        count = int(result.getOutput(0))
        arcpy.AddMessage("Total Number of Records: " + str(count))

        if count > 0:
            if stage == "Interim":
                arcpy.AddMessage("Copying " + layerType + " records to FWS Deliverable Stage " +
                             tes_rank + " Geodatabase as " + outputfilename)
            else:
                arcpy.AddMessage("Copying " + layerType + " records to Final Stage " +
                             tes_rank + " Geodatabase as " + outputfilename)
            arcpy.CopyFeatures_management("tmplyr", outlocation)
        else:
            arcpy.AddMessage("No records found for rank " + tes_rank)

    arcpy.AddMessage("Complete copying data to " + stage + " staging GDB")
    arcpy.AddMessage(" ____________________________________________________________________")
    return


def unitid_dissolve(filename):
    arcpy.AddMessage(" ____________________________________________________________________")

    arcpy.AddMessage("Updating UnitID field from intersection")

    cur = arcpy.UpdateCursor(filename)

    field = "UnitID_FS"
    fieldother = "Type"
    fieldspecies = "SNAME_FIRE"
    plant0512num = 0

    # populating UnitID field with UnitID_FS field
    for row in cur:
        row.UnitID = "0" + str(row.getValue(field))
        cur.updateRow(row)
        # Used for deleting all the plant records in San Bernardino for CNDDB
        if layerType == "CNDDB":
            if str(row.getValue(field)) == "512" and row.getValue(fieldother) == "PLANT":
                cur.deleteRow(row)
                plant0512num += 1
                arcpy.AddMessage("deleted a row for 0512 Plant: " + row.getValue(fieldspecies))

    del cur

    # running export to gdb just for CNDDB dataset others were ran prior to this function
    if layerType == "CNDDB":
        arcpy.AddMessage("Total records deleted because they were Plants from San Bernardino : " + str(plant0512num))
        copy_to_gdb("Interim", filename)

    # if layerType == "CNDDB":
    #     with arcpy.da.UpdateCursor(intersectFeatureClass, ["Type", "UnitID"]) as cursor:
    #         for row in cursor:
    #             if row[0] == "PLANT" and row[1] == "0512":
    #                 cursor.deleteRow()
    #                 arcpy.AddMessage("Deleted row")

    arcpy.AddMessage("Repairing Geometry ......")
    arcpy.RepairGeometry_management(filename)

    arcpy.AddMessage("Dissolving Features")

    dissolveFeatureClass = filename + "_dissolved"

    arcpy.PairwiseDissolve_analysis(intersectFeatureClass, dissolveFeatureClass,
                              ["UnitID", "GRANK_FIRE", "SNAME_FIRE", "CNAME_FIRE", "SOURCEFIRE",
                               "BUFFT_FIRE", "BUFFM_FIRE", "CMNT_FIRE", "INST_FIRE"])

    # arcpy.Dissolve_management(filename, dissolveFeatureClass,
    #                                 ["UnitID", "GRANK_FIRE", "SNAME_FIRE", "CNAME_FIRE", "SOURCEFIRE",
    #                                  "BUFFT_FIRE", "BUFFM_FIRE", "CMNT_FIRE", "INST_FIRE"], "", "SINGLE_PART")

    # May delete this once I confirm we don't need BUFF_DIST from Stacey
    # arcpy.PairwiseDissolve_analysis(intersectFeatureClass, dissolveFeatureClass,
    #                                 ["UnitID", "GRANK_FIRE", "SNAME_FIRE", "CNAME_FIRE", "SOURCEFIRE",
    #                                  "BUFFT_FIRE", "BUFFM_FIRE", "CMNT_FIRE", "INST_FIRE", "BUFF_DIST"])

    arcpy.AddMessage("Repairing Dissolved Geometry ......")
    arcpy.RepairGeometry_management(filename)
    arcpy.AddMessage("Dissolve and Repair complete")
    arcpy.AddMessage(" ____________________________________________________________________")

    return dissolveFeatureClass


try:

    # if layerType == "Local":
    if layerType == "Local" or layerType == "NOAA_ESU":
        fcList = arcpy.ListFeatureClasses()

        for fc in fcList:
            arcpy.AddMessage("  fc: " + fc)
            if layerType == "NOAA_ESU":
                if not fc.endswith('_AllHydro'):
                    continue
            arcpy.AddMessage("--------------------------------------------------")
            arcpy.AddMessage("Intersecting " + fc)
            outFeatClass = fc

            usfsOwnershipFeatureClass = in_workspace + \
                                        "\\USFS_Ownership_LSRS\\2017_USFS_Ownership_CAALB83.gdb\\USFS_OwnershipLSRS_2017"

            intersectFeature = outFeatClass + "_intersect"

            arcpy.AddMessage("Intersecting with USFS Ownership feature class .....")
            arcpy.AddMessage("Please be patient while this runs .....")

            if layerType == "Local":
                intersectFeatureClass = intersectFeatureDataset + "\\" + intersectFeature
            else:
                intersectFeatureClass = noaaGdb + "\\" + intersectFeature

            if layerType == "Local":
                arcpy.Intersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)
            else:
                arcpy.PairwiseIntersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)

            arcpy.AddMessage("Completed Intersection")

            copy_to_gdb("Interim", intersectFeatureClass)

            dissolveFC = unitid_dissolve(intersectFeatureClass)

            copy_to_gdb("Final", dissolveFC)
    else:

        usfsOwnershipFeatureClass = in_workspace + \
                                    "\\USFS_Ownership_LSRS\\2017_USFS_Ownership_CAALB83.gdb\\USFS_OwnershipLSRS_2017"

        intersectFeatureClass = outFeatClass + "_intersect"

        arcpy.AddMessage("Intersecting with USFS Ownership feature class .....")
        arcpy.AddMessage("Please be patient while this runs .....")

        # arcpy.Intersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)

        arcpy.PairwiseIntersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)

        arcpy.AddMessage("Completed Intersection")

        # CNDDB layer is skipped here because we need to remove BDF plants prior to exporting GDB
        if layerType != "CNDDB":
            # may need to fix the NOAA layer - may remove this and just use the above
            if layerType == "NOAA_ESU":
                copy_to_gdb("Interim", nameOfFile)
            else:
                copy_to_gdb("Interim", intersectFeatureClass)

        dissolveFC = unitid_dissolve(intersectFeatureClass)

        # may need to fix the NOAA layer - may remove this and just use the above
        if layerType == "NOAA_ESU":
            copy_to_gdb("Final", dissolveFC)
        else:
            copy_to_gdb("Final", dissolveFC)

    arcpy.AddMessage("Completed Script successfully!!")

except arcpy.ExecuteError:
    arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
    arcpy.AddMessage(e)