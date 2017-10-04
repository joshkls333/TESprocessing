# ---------------------------------------------------------------------------
# total_run.py
#
# Description: Combines the select_tes_layer.py and pairwise_intersection.py
#              programs so a user could run the 5 select layers in one run.
# ---------------------------------------------------------------------------
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
# ---------------------------------------------------------------------------
# pairwise_intersect.py
#
# Usage: PairwiseIntersect_analysis
# Description: Performs an Intersect_analysis with pairwise processing that only
#              runs in ArcGIS Pro. After the intersection data is exported to FWS GDB.
#              UnitID field is populated based on intersection and a Dissolve is performed
#              to dissolve data and remove extraneous fields. Data is exported to Final
#              GDB.
#              Note: User selects final file from preprocessing for all datasets except Local
#                     and NOAA. Those two datasets will generate a list of feature classes and
#                     loop through them running intersection and export processes.
#
# Runtime Estimates: NOAA       : 29 min 52 sec
#                    Local      : 16 min 20 sec
#                    TESP       :  1 min  2 sec
#                    Wild Sites :        33 sec
#                    Wild Obs E :  2 min 16 sec
#                    Wild Obs T :  1 min  4 sec
#                    Wild obs S :        22 sec
#                    CHab Poly  :        26 sec
#                    Chab Line  :        11 sec
#                    CNDDB      :        48 sec
#                    Cond Nest  :        18 sec
#                    Cond Hack  :        16 sec
#
# Created by: Josh Klaus 08/01/2017 jklaus@fs.fed.us
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import sys
import csv
import os
import datetime
import subprocess

# Set workspace or obtain from user input
# in_workspace = "C:\\Users\\jklaus\\Documents\\Python_Testing\\fire_retardant\\"
in_workspace = sys.argv[1]

arcpy.env.workspace = in_workspace
arcpy.env.overwriteOutput = True

# using the now variable to assign year everytime there is a hardcoded 2017
now = datetime.datetime.today()
curMonth = str(now.month)
curYear = str(now.year)
arcpy.AddMessage("Year is " + curYear)

sciNameField = ""
commonNameField = ""
sourceField = ""

# -------------------------------------------------------------------------------
# the following section will create folders and geodatabases to store Deliverables
# for different stages of the processing of the individual databases
# -------------------------------------------------------------------------------

tesvariablelist = ["Endangered", "Threatened", "Sensitive"]

for tes in tesvariablelist:
    newPath = in_workspace + "\\" + curYear + "_" + tes
    tesGDB = curYear + "_FRA_" + tes + "_OriginalDataNoBuffers_FWSDeliverable_CAALB83.gdb"

    if not os.path.exists(newPath):
        arcpy.AddMessage("Creating directory for " + tes + " Data Deliverables ....")
        os.makedirs(newPath)
        arcpy.AddMessage("Creating Geodatabase for " + tes + " Data Deliverables ....")
        arcpy.CreateFileGDB_management(newPath, tesGDB)

# --------------------------------------------------------------------------------
#  Please note the following selections of inTable and csv are file dependent
# --------------------------------------------------------------------------------

layerType = sys.argv[4]

# layerType = "Wildlife_Sites"

outputDir = in_workspace + "\\" + "Output"
if not os.path.exists(outputDir):
    arcpy.AddMessage("Creating directory for Output")
    os.makedirs(outputDir)

if not os.path.exists(outputDir + "\\" + layerType):
    arcpy.AddMessage("Creating output directory for " + layerType)
    os.makedirs(outputDir + "\\" + layerType)

layerWorkSpace = outputDir + "\\" + layerType + "\\"
projectedGDB = layerType + "_Test_" + curYear + "_CAALB83_newproj.gdb"
foundFC = layerType + "_" + curYear + "_original"

arcpy.AddMessage("Layer Type: " + layerType)

#-------------------------------------------------------------------------------------------
# the below is hardcoded values used for testing and debugging
# inTable = in_workspace

inTable = sys.argv[2]


# if layerType == "TESP":
#     inTable += "\\USFS_EDW\\EDW_TESP_r05_021617_Everything.gdb\\TESP\\TESP_OccurrenceAll"
# elif layerType == "Wildlife_Sites":
#     inTable += "\\USFS_EDW\\EDW_FishWildlife_R05_021617_Everything.gdb\\Fish_and_Wildlife\\WildlifeSites"
# elif layerType == "Wildlife_Observations":
#     inTable += "\\USFS_EDW\\EDW_FishWildlife_R05_021617_Everything.gdb\\Fish_and_Wildlife\\FishWildlife_Observation"
# elif layerType == "Critical_Habitat_Lines":
#     inTable += "\\CHab\\crithab_all_layers\\CRITHAB_LINE.shp"
# elif layerType == "Critical_Habitat_Polygons":
#     inTable += "\\CHab\\crithab_all_layers\\CRITHAB_POLY.shp"
# elif layerType == "CNDDB":
#     inTable += "\\CNDDB\\gis_gov\\cnddb.shp"

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

csvFile = sys.argv[3]

# csvFile = in_workspace + "\\csv_tables"
#
# if layerType == "TESP":
#     csvFile += "\\TESP_SummaryTable.csv"
# elif layerType == "Wildlife_Sites":
#     csvFile += "\\Wildlife_Sites_SummaryTable.csv"
# elif layerType == "Wildlife_Observations":
#     csvFile += "\\Wildlife_Observations_SummaryTable.csv"
# elif layerType == "Critical_Habitat_Polygons":
#     csvFile += "\\crithab.csv"
# elif layerType == "Critical_Habitat_Lines":
#     csvFile += "\\crithab.csv"
# elif layerType == "CNDDB":
#     csvFile += "\\CNDDB_SummaryTable.csv"

arcpy.AddMessage("csv File: " + csvFile)
arcpy.AddMessage("NOTE: Code will operate differently for csv in Pro vs 10.x!!!!!")
arcpy.AddMessage("Version of Python: " + sys.version)

if sys.version_info[0] < 3:
    # uncomment when using arcgis 10.3
    with open(csvFile, 'rb') as f:
        reader = csv.reader(f)
        selectionList = list(reader)
else:
    # use when using arcgis pro
    with open(csvFile) as f:
        reader = csv.reader(f)
        selectionList = list(reader)

arcpy.AddMessage("Listing of csv table data: ")
for item in selectionList:
    arcpy.AddMessage("  " + str(item))

pulldate = curMonth + "/" + curYear

if layerType == "TESP":
    sciNameField = "SCIENTIFIC_NAME"
    commonNameField = "ACCEPTED_COMMON_NAME"
    sourceField = "EDW TESP OccurrencesALL_FoundPlant pulled " + pulldate
elif layerType == "Wildlife_Sites":
    sciNameField = "SCI_NAME"
    commonNameField = "COMMON_NAME"
    sourceField = "EDW Wildlife Sites pulled " + pulldate
elif layerType == "Wildlife_Observations":
    sciNameField = "SCIENTIFIC_NAME"
    commonNameField = "COMMON_NAME"
    sourceField = "EDW OBS FishWildlife pulled " + pulldate
elif layerType == "Critical_Habitat_Polygons":
    sciNameField = "sciname"
    commonNameField = "comname"
    sourceField = "FWS Critical Habitat pulled " + pulldate
elif layerType == "Critical_Habitat_Lines":
    sciNameField = "sciname"
    commonNameField = "comname"
    sourceField = "FWS Critical Habitat pulled " + pulldate
elif layerType == "CNDDB":
    sciNameField = "SNAME"
    commonNameField = "CNAME"
    sourceField = "CA CNDDB GOV version pulled " + pulldate

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
                            row.INST_FIRE = "CNDDB ACCURACY is GT 300 ft buffer - minimum 3 ft buffer applied"
                        elif item[2] == "600":
                            bufferAmount = 72
                            row.INST_FIRE = "CNDDB ACCURACY is 529 ft - 72 ft buffer applied to meet 600 ft requirement"
                    elif accuracy == "1/5 mile":
                        if item[2] == "300":
                            bufferAmount = 3
                            row.INST_FIRE = "CNDDB ACCURACY is GT 300 ft buffer - minimum 3 ft buffer applied"
                        elif item[2] == "600":
                            bufferAmount = 3
                            row.INST_FIRE = "CNDDB ACCURACY is GT 600 ft buffer - minimum 3 ft buffer applied"
                    elif accuracy == "80 meters":
                        if item[2] == "300":
                            bufferAmount = 38
                            row.INST_FIRE = "CNDDB ACCURACY is LT 300 ft buffer - adding 38 ft"
                        elif item[2] == "600":
                            bufferAmount = 338
                            row.INST_FIRE = "CNDDB ACCURACY is 262 ft - 338 ft buffer applied to meet 600 ft"
                    elif accuracy == "specific area":
                        bufferAmount = int(item[2])
                        row.INST_FIRE = "CNDDB ACCURACY is specific - adding " + item[2] + " ft buffer"
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

                elif item[0].startswith(speciesrow) and item[3] == forestrow:
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

    tesRankList = ["Endangered", "Threatened", "Sensitive"]

    for tesRank in tesRankList:
        arcpy.MakeFeatureLayer_management(selectFC, "lyr")

        arcpy.AddMessage("Selecting records based on " + tesRank + " rank ....")
        arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "GRANK_FIRE = '" + tesRank + "'")

        outlocation = in_workspace + "\\" + curYear + "_" + tesRank + "\\" + curYear + "_FRA_" + \
                      tesRank + "_OriginalDataNoBuffers_FWSDeliverable_CAALB83.gdb" + "\\"

        if layerType == "TESP":
            outlocation += "EDW_TESP_" + curYear + "_" + tesRank + "_OccurrenceAll_FoundPlants_nobuf"
        elif layerType == "Wildlife_Sites":
            outlocation += "EDW_WildlifeSites_" + curYear + "_" + tesRank + "_nobuf"
        elif layerType == "Wildlife_Observations":
            outlocation += "EDW_FishWildlife_Observation_" + curYear + "_" + tesRank + "_nobuf"
        elif layerType == "Critical_Habitat_Polygons":
            outlocation += "CHabPolyAllSelectedSpecies_" + curYear + "_" + tesRank + "_nobuf"
        elif layerType == "Critical_Habitat_Lines":
            outlocation += "CHabLineAllSelectedSpecies_" + curYear + "_" + tesRank + "_nobuf"
        elif layerType == "CNDDB":
            outlocation += "CNDDB_selects_" + curYear + "_" + tesRank + "_nobuf"

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
    interimfc = newProjectWorkSpace + "_interim"

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

        arcpy.CopyFeatures_management(singlePartBufferedFC, interimfc)

    if layerType == "CNDDB":

        arcpy.AddMessage("Moving Shasta Crayfish files into Geodatabase")
        # May need to change where this is being pulled
        tempWorkSpace = in_workspace + "\\" + "CNDDB" + "\\" + curYear + "_CNDDB_CAALB83.gdb\\"
        crayFlowLines = tempWorkSpace + "CNDDB_Endangered_ShastaCrayfish_NHDFlowlines"
        crayWaterBodies = tempWorkSpace + "CNDDB_Endangered_ShastaCrayfish_NHDWaterbodies"
        arcpy.FeatureClassToGeodatabase_conversion([crayFlowLines, crayWaterBodies], projGDB)

        arcpy.AddMessage("Merging the CNDDDB feature class with the Shasta Crayfish files")
        arcpy.Merge_management([crayFlowLines, crayWaterBodies, singlePartBufferedFC], siteMerge)
        arcpy.AddMessage("Finished with merge")

        arcpy.AddMessage("Repairing Geometry of merged layer")
        arcpy.RepairGeometry_management(siteMerge)

        arcpy.CopyFeatures_management(siteMerge, interimfc)

    elif layerType == "Wildlife_Observations":

        arcpy.AddMessage("Breaking up into three layers prior to intersect")
        arcpy.MakeFeatureLayer_management(singlePartBufferedFC, "lyr")

        tesRankList = ["Endangered", "Threatened", "Sensitive"]

        for tesRank in tesRankList:
            finalWorkSpace = layerWorkSpace + "\\" + projectedGDB + "\\" + \
                             "EDW_FishWildlife_Observation_" + curYear + "_" + tesRank[:1]

            arcpy.AddMessage("Selecting records based on " + tesRank + " rank ....")
            arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "GRANK_FIRE = '" + tesRank + "'")
            arcpy.AddMessage("Copying selected records to " + tesRank + " Feature Class ......")
            arcpy.CopyFeatures_management("lyr", finalWorkSpace)

    elif layerType == "Wildlife_Sites":
        arcpy.AddMessage("Moving two MYLF study area files into Geodatabase")
        # May need to fix where this data is being pulled
        tmpWorkSpace = in_workspace + "\\" + "USFS_EDW" + "\\" + curYear + "_EDW_CAALB83.gdb\\"
        studyFlowLines = tmpWorkSpace + \
                         "EDW_WildlifeSites_FRASelectionSet_CAALB_NHDFlowlines_MYLF_E_INFStudyAreas_buffered"
        studyWaterBodies = tmpWorkSpace + \
                           "EDW_WildlifeSites_FRASelectionSet_CAALB_NHDWaterbodys_MYLF_E_INFStudyAreas_buffered"
        arcpy.FeatureClassToGeodatabase_conversion([studyFlowLines, studyWaterBodies], projGDB)

        arcpy.AddMessage("Merging the Wildlife Sites feature class with the two MYLF study area")
        arcpy.Merge_management([studyFlowLines, studyWaterBodies, singlePartBufferedFC], siteMerge)
        arcpy.AddMessage("Finished with merge")

        arcpy.AddMessage("Repairing Geometry of merged layer")
        arcpy.RepairGeometry_management(siteMerge)

        arcpy.CopyFeatures_management(siteMerge, interimfc)

        os.system("pairwise_intersect.py " + in_workspace + " " + siteMerge + " " + layerType)

    if layerType == "Wildlife_Observations":
        arcpy.AddMessage("Ensure the removal of Acipenser medirostris from SRF due to bad data!!!!")
    arcpy.AddMessage("Script complete ... check data and make changes ... then proceed to intersection")

    arcpy.AddMessage("interimfc: " + interimfc)

    cmd = "pairwise_intersect.py " + " C:\\Users\\jklaus\\Documents\\Python_Testing\\fire_retardant\\" + " " + interimfc + " " + "TESP"

    arcpy.AddMessage(cmd)

    subprocess.call(cmd)

    arcpy.AddMessage(" What happened???")

except arcpy.ExecuteError:
    arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
    arcpy.AddMessage(e)
