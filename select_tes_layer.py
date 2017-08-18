# select_tes_layer.py
#
# Usage: select_fields
# Description: Selects only those records with Scientific Names equal to TES list
# Created by: Josh Klaus 07/27/2017 jklaus@fs.fed.us
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import sys
import csv
import os

# Set workspace or obtain from user input
in_workspace = "C:\\Users\\jklaus\\Documents\\Python_Testing\\fire_retardant\\"
# in_workspace = sys.argv[1]

arcpy.env.workspace = in_workspace
arcpy.env.overwriteOutput = True

# -------------------------------------------------------------------------------
# the following section will create folders and geodatabases to store Deliverables
# for different stages of the processing of the individual databases
# -------------------------------------------------------------------------------

newPath_threatened = in_workspace + "2017_Threatened"
threatened_gdb = "2017_FRA_Threatened_OriginalDataNoBuffers_FWSDeliverable_CAALAB83.gdb"
newPath_endangered = in_workspace + "2017_Endangered"
endangered_gdb = "2017_FRA_Endangered_OriginalDataNoBuffers_FWSDeliverable_CAALAB83.gdb"
newPath_sensitive  = in_workspace + "2017_Sensitive"
sensitive_gdb = "2017_FRA_Sensitive_OriginalDataNoBuffers_FWSDeliverable_CAALAB83.gdb"

if not os.path.exists(newPath_threatened):
    arcpy.AddMessage("Creating directory for Threatened Data Deliverables ....")
    os.makedirs(newPath_threatened)
    arcpy.AddMessage("Creating Geodatabase for Threatened Data Deliverables ....")
    arcpy.CreateFileGDB_management(newPath_threatened, threatened_gdb)

if not os.path.exists(newPath_endangered):
    arcpy.AddMessage("Creating directory for Endangered Data Deliverables ....")
    os.makedirs(newPath_endangered)
    arcpy.AddMessage("Creating Geodatabase for Endangered Data Deliverables ....")
    arcpy.CreateFileGDB_management(newPath_endangered, endangered_gdb)

if not os.path.exists(newPath_sensitive):
    arcpy.AddMessage("Creating directory for Sensitive Data Deliverables ....")
    os.makedirs(newPath_sensitive)
    arcpy.AddMessage("Creating Geodatabase for Sensitive Data Deliverables ....")
    arcpy.CreateFileGDB_management(newPath_sensitive, sensitive_gdb)

# --------------------------------------------------------------------------------
#  Please note the following selections of inTable and csv are file dependent
# --------------------------------------------------------------------------------

# inTable = sys.argv[2]

# layerType = sys.argv[4]

layerType = "CNDDB"

layerWorkSpace = in_workspace + "\\" + layerType + "\\"
projectedGDB = layerType + "_Test_2017_CAALB83_newproj.gdb"
foundFC = layerType + "_2017_Occurrence_found"

arcpy.AddMessage("Layer Type: " + layerType)

#  Need to clean up how to set up workspaces especially if these layers need to be projected
#-------------------------------------------------------------------------------------------

inTable = in_workspace

# if inTable == "#":
if layerType == "TESP":
    inTable += "\\TESP\\EDW_TESP_r05_021617_Everything.gdb\\TESP\\TESP_OccurrenceAll"
elif layerType == "Wildlife_Sites":
    inTable += "\\Wildlife\\EDW_FishWildlife_R05_021617_Everything.gdb\\Fish_and_Wildlife\\WildlifeSites"
elif layerType == "Wildlife_Observations":
    inTable += "\\Wildlife\\EDW_FishWildlife_R05_021617_Everything.gdb\\Fish_and_Wildlife\\FishWildlife_Observation"
elif layerType == "Critical_Habitat_Lines":
    inTable += "\\CHab\\crithab_all_layers\\CRITHAB_LINE.shp"
elif layerType == "Critical_Habitat_Polygons":
    inTable += "\\CHab\\crithab_all_layers\\CRITHAB_POLY.shp"
elif layerType == "Critical_Habitat_Lines":
    inTable += "\\CHab\\2017_CHab_CAALB83.gdb\\CHabLineAllSelectedSpecies2017"
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


# if layerType == "Critical_Habitat_Polygons" or layerType == "CNDDB":
#     selectFC = newspace + "_new"
# else:
#     selectFC = inTable + "_new"

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

arcpy.AddField_management(newProjectWorkSpace, "UnitID", "TEXT", "", "", "5", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(newProjectWorkSpace, "GRANK_FIRE", "TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(newProjectWorkSpace, "SOURCEFIRE", "TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(newProjectWorkSpace, "SNAME_FIRE", "TEXT", "", "", "60", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(newProjectWorkSpace, "CNAME_FIRE", "TEXT", "", "", "60", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(newProjectWorkSpace, "BUFFT_FIRE", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(newProjectWorkSpace, "BUFFM_FIRE", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(newProjectWorkSpace, "CMNT_FIRE", "TEXT", "", "", "150", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(newProjectWorkSpace, "INST_FIRE", "TEXT", "", "", "150", "", "NULLABLE", "NON_REQUIRED", "")


# Note the different ways of bringing in a csv for lookup data on the buffer amount, forest, and status
# _____________________________________________________________________________________________________

csvFile = in_workspace + "\\csv_tables"

# csvFile = sys.argv[3]

# if csvFile == "#":

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

with open(csvFile, 'rb') as f:
    reader = csv.reader(f)
    selectionList = list(reader)

arcpy.AddMessage("Listing of csv table data: ")
for item in selectionList:
    arcpy.AddMessage("  " + str(item))

if layerType == "TESP":
    sciNameField = "SCIENTIFIC_NAME"
    commonNameField = "ACCEPTED_COMMON_NAME"
    sourceField = "EDW TESp OccurrencesALL_FoundPlant pulled 2/2017"
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

# Builds the selection query used in SelectLayerByAttribute_management
# customized based on what the Scientific name field is
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
    selectQuery += " AND (TOTAL_DETECTED <> 0)"
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

sqLength = int(len(selectQuery))
n = int(round(len(selectQuery) / 100))

arcpy.AddMessage("The Selection Query will be : " )
arcpy.AddMessage("  " + selectQuery[0:n])
arcpy.AddMessage("  " + selectQuery[n:n+100])
arcpy.AddMessage("  " + selectQuery[n+100:n+200])
arcpy.AddMessage("  " + selectQuery[n+200:n+300])
arcpy.AddMessage("  " + selectQuery[n+300:n+400])
arcpy.AddMessage("  " + selectQuery[n+400:n+800])
arcpy.AddMessage("  " + selectQuery[n+800:sqLength-100])
arcpy.AddMessage("  " + selectQuery[n+800:sqLength-100])
arcpy.AddMessage("  " + selectQuery[sqLength-100:sqLength])

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

        newpath_sensitive = in_workspace + "2017_Sensitive"
        sensitive_gdb = "2017_FRA_Sensitive_OriginalDataNoBuffers_FWSDeliverable_CAALAB83.gdb"

        outlocation = in_workspace + "2017_" + tesRank + "\\" + "2017_FRA_" + \
                      tesRank + "_OriginalDataNoBuffers_FWSDeliverable_CAALAB83.gdb" + "\\"

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

    singlePartFeatureClass = selectFC + "_singlepart"

    arcpy.AddMessage("Converting multipart geometry to singlepart .....")

    arcpy.MultipartToSinglepart_management(selectFC, singlePartFeatureClass)

    inCount = int(arcpy.GetCount_management(selectFC).getOutput(0))
    outCount = int(arcpy.GetCount_management(singlePartFeatureClass).getOutput(0))

    arcpy.AddMessage("Number of new records: " + str(outCount - inCount))

    arcpy.AddMessage("Repairing Geometry ......")
    arcpy.RepairGeometry_management(singlePartFeatureClass)

    bufferFC = selectFC + "_buffer"
    singlePartBufferedFC = bufferFC + "_buffered_spart"

    if layerType != "Critical_Habitat_Polygons" or layerType != "Critical_Habitat_Lines":
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

    if layerType == "Wildlife_Observations":
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
