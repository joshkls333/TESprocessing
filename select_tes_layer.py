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
#  Please note the following selections of intable and csv are file dependent
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

inTable = ""

# if inTable == "#":
if layerType == "TESP":
    inTable = in_workspace + "\\TESP\\EDW_TESP_r05_021617_Everything.gdb\\TESP\\TESP_OccurrenceAll"

#    attempting to make a generic layerworkspace that I can use for all layers
#    layerWorkSpace = in_workspace + "\\" + layerType + "\\"
#    projectedGDB = "Test_2017_TESP_CAALB83_newproj.gdb"
#    selectFC = "EDW_TESP_2017_OccurrenceAll_Found"

elif layerType == "Wildlife_Sites":
    inTable = in_workspace + "\\Wildlife\\EDW_FishWildlife_R05_021617_Everything.gdb\\Fish_and_Wildlife\\WildlifeSites"
elif layerType == "Wildlife_Observations":
    inTable = in_workspace + "\\Wildlife\\EDW_FishWildlife_R05_021617_Everything.gdb\\Fish_and_Wildlife\\FishWildlife_Observation"
elif layerType == "Critical_Habitat_Polygons":
    inTable = in_workspace + "\\CHab\\crithab_all_layers\\CRITHAB_POLY.shp"
elif layerType == "Critical_Habitat_Lines":
    inTable = in_workspace + "\\CHab\\2017_CHab_CAALB83.gdb\\CHabLineAllSelectedSpecies2017"
elif layerType == "CNDDB":
    inTable = in_workspace + "\\CNDDB\\gis_gov\\cnddb.shp"

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

arcpy.AddMessage("Data: " + inTable)

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

csvFile = in_workspace

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
elif layerType == "CNDDB":
    csvFile += "\\CNDDB_SummaryTable.csv"

arcpy.AddMessage("csv File: " + csvFile)

with open(csvFile, 'rb') as f:
    reader = csv.reader(f)
    selectionList = list(reader)

arcpy.AddMessage("Listing of csv table data: ")
for item in selectionList:
    arcpy.AddMessage("  " + item)

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
elif layerType == "CNDDB":
    sciNameField = "SNAME"
    commonNameField = "CNAME"
    sourceField = 'CA CNDDB GOV version pulled 2/2017'

# Builds the selection query used in SelectLayerByAttribute_management
# customized based on what the Scientific name field is
selectQuery =  "(" + sciNameField + " = "

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
    selectQuery += " AND (TOTAL_DETECTED != 0)"

# Need to test the below for TESP layer with added searches for ACCEPTED_SCIENTIFIC_NAME
# __________________________________________________________________________________________________
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

n = round(len(selectQuery) / 10)

arcpy.AddMessage("The Selection Query will be : " )
arcpy.AddMessage("  " + selectQuery[0:n])
arcpy.AddMessage("  " + selectQuery[n:n+10])
arcpy.AddMessage("  " + selectQuery[n+10:n+20])
arcpy.AddMessage("  " + selectQuery[n+20:n+30])
arcpy.AddMessage("  " + selectQuery[n+30:n+40])
arcpy.AddMessage("  " + selectQuery[n+40:n+50])
arcpy.AddMessage("  " + selectQuery[n+50:len(selectQuery)])

# -----------------------------------------------------------------------------------------

try:

    arcpy.MakeFeatureLayer_management(newProjectWorkSpace, "lyr" )

    arcpy.AddMessage("-----------------")
    arcpy.AddMessage("Selection: " + selectQuery)
    arcpy.AddMessage("-----------------")

    arcpy.AddMessage("Selecting layers based on selection ....")
    arcpy.SelectLayerByAttribute_management ("lyr", "NEW_SELECTION", selectQuery )

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

    if layerType == "Critical_Habitat_Polygons":
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

    arcpy.AddMessage("Number of Threatened = " + str(threatNum))
    arcpy.AddMessage("Number of Sensitive = " + str(sensitiveNum))
    arcpy.AddMessage("Number of Endangered = " + str(endangerNum))
    arcpy.AddMessage("Number of Other = " + str(otherNum))

    arcpy.AddMessage("Splitting current state of data into deliverable Geodatabases .....")

#    does not work in ArcGIS only ArcGIS Pro
#    arcpy.SplitByAttributes_analysis(selectFC, sensitive_gdb, "GRANK_FIRE")

#    status_fc = intable + "_noAAAbuf"

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
        elif layerType == "CNDDB":
            outlocation += "CNDDB_selects_2017_" + tesRank + "_nobuf"

        result = arcpy.GetCount_management("lyr")
        count = int(result.getOutput(0))
        arcpy.AddMessage("Total Number of Records: " + str(count))

        if count > 0:
            arcpy.AddMessage("Copying selected records to " + tesRank + " Geodatabase ......")
            arcpy.CopyFeatures_management("lyr", outlocation)
#
#     #--------------Copying to Sensitive Geodatabase for interim deliverable step
#     arcpy.MakeFeatureLayer_management(selectFC, "lyr" )
#
#     arcpy.AddMessage("Selecting records based on Sensitive rank ....")
#     arcpy.SelectLayerByAttribute_management ("lyr", "NEW_SELECTION", "GRANK_FIRE = 'Sensitive'" )
#
#     newpath_sensitive = in_workspace + "2017_Sensitive"
#     sensitive_gdb = "2017_FRA_Sensitive_OriginalDataNoBuffers_FWSDeliverable_CAALAB83.gdb"
#
#     outlocation = newpath_sensitive + "\\" + sensitive_gdb + "\\"
#     if layerType == "TESP":
#         outlocation += "EDW_TESP_2017_Sensitive_OccurrenceAll_FoundPlants_nobuf"
#     elif layerType == "Wildlife_Sites":
#         outlocation += "EDW_WildlifeSites_2017_Sensitive_nobuf"
#     elif layerType == "Wildlife_Observations":
#         outlocation += "EDW_FishWildlife_Observation_2017_Sensitive_nobuf"
#     elif layerType == "Critical_Habitat_Polygons":
#         outlocation += "CHabPolyAllSelectedSpecies_2017_Sensitive_nobuf"
#     elif layerType == "CNDDB":
#         outlocation += "CNDDB_selects_2017_Sensitive_nobuf"
#
#     arcpy.AddMessage("Copying selected records to Sensitive Geodatabase ......")
#     arcpy.CopyFeatures_management("lyr", outlocation)
#
#     result = arcpy.GetCount_management(outlocation)
#     count = int(result.getOutput(0))
#     arcpy.AddMessage("Total Number of Records: " + str(count))
#
# #--------------Copying to Threatened Geodatabase for interim deliverable step
#
#     arcpy.MakeFeatureLayer_management(selectFC, "lyr" )
#
#     arcpy.AddMessage("Selecting records based on Threatened rank ....")
#     arcpy.SelectLayerByAttribute_management ("lyr", "NEW_SELECTION", "GRANK_FIRE = 'Threatened'" )
#
#     outlocation = newpath_threatened + "\\" + threatened_gdb + "\\"
#
#     if layerType == "TESP":
#         outlocation += "EDW_TESP_2017_Threatened_OccurrenceAll_FoundPlants_nobuf"
#     elif layerType == "Wildlife_Sites":
#         outlocation += "EDW_WildlifeSites_2017_Threatened_nobuf"
#     elif layerType == "Wildlife_Observations":
#         outlocation += "EDW_FishWildlife_Observation_2017_Threatened_nobuf"
#     elif layerType == "Critical_Habitat_Polygons":
#         outlocation += "CHabPolyAllSelectedSpecies_2017_Threatened_nobuf"
#     elif layerType == "CNDDB":
#         outlocation += "CNDDB_selects_2017_Threatened_nobuf"
#
#     arcpy.AddMessage("Copying selected records to Threatened Geodatabase ......")
#     arcpy.CopyFeatures_management("lyr", outlocation)
#
#     result = arcpy.GetCount_management(outlocation)
#     count = int(result.getOutput(0))
#     arcpy.AddMessage("Total Number of Threatened Records: " + str(count))
#
# #--------------Copying to Endangered Geodatabase for interim deliverable step
#     arcpy.MakeFeatureLayer_management(selectFC, "lyr" )
#
#     arcpy.AddMessage("Selecting records based on Endangered rank ....")
#     arcpy.SelectLayerByAttribute_management ("lyr", "NEW_SELECTION", "GRANK_FIRE = 'Endangered'" )
#
#     outlocation = newpath_endangered + "\\" + endangered_gdb + "\\"
#
#     if layerType == "TESP":
#         outlocation += "EDW_TESP_2017_Endangered_OccurrenceAll_FoundPlants_nobuf"
#     elif layerType == "Wildlife_Sites":
#         outlocation += "EDW_WildlifeSites_2017_Endangered_nobuf"
#     elif layerType == "Wildlife_Observations":
#         outlocation += "EDW_FishWildlife_Observation_2017_Endangered_nobuf"
#     elif layerType == "Critical_Habitat_Polygons":
#         outlocation += "CHabPolyAllSelectedSpecies_2017_Endangered_nobuf"
#     elif layerType == "CNDDB":
#         outlocation += "CNDDB_selects_2017_Endangered_nobuf"
#
#     arcpy.AddMessage("Copying selected records to Endangered Geodatabase ......")
#     arcpy.CopyFeatures_management("lyr", outlocation)
#
#     result = arcpy.GetCount_management(outlocation)
#     count = int(result.getOutput(0))
#     arcpy.AddMessage("Total Number of Endangered Records: " + str(count))
#
# ----------------------------------------------------------------------
# Tested below pieces - commenting out to test attribution
# ----------------------------------------------------------------------
    outFeatureClass = selectFC + "_singlepart"

    arcpy.AddMessage("Converting multipart geometry to singlepart .....")

    arcpy.MultipartToSinglepart_management(selectFC, outFeatureClass)

    inCount = int(arcpy.GetCount_management(selectFC).getOutput(0))
    outCount = int(arcpy.GetCount_management(outFeatureClass).getOutput(0))

    arcpy.AddMessage("Number of new records: " + str(outCount - inCount))

    arcpy.AddMessage("Repairing Geometry ......")
    arcpy.RepairGeometry_management(outFeatureClass)

    if layerType != "Critical_Habitat_Polygons":
        arcpy.AddMessage("Buffering features ....")
        buffer_fc = outFeatureClass + "_buffer"
        buffer_field = "BUFFM_FIRE"
        arcpy.Buffer_analysis(outFeatureClass, buffer_fc, buffer_field)

        outFeatClass = buffer_fc + "_spart"

        arcpy.AddMessage("Converting buffer layer from multipart geometry to singlepart .....")

        arcpy.MultipartToSinglepart_management(buffer_fc, outFeatClass)

        inCount = int(arcpy.GetCount_management(buffer_fc).getOutput(0))
        outCount = int(arcpy.GetCount_management(outFeatClass).getOutput(0))

        arcpy.AddMessage("Number of new records: " + str(outCount - inCount))

        arcpy.AddMessage("Repairing Geometry of singlepart buffer layer ......")
        arcpy.RepairGeometry_management(outFeatClass)

    if layerType == "Wildlife_Observations":
        arcpy.AddMessage("Breaking up into three layers prior to intersect")
        arcpy.MakeFeatureLayer_management(outFeatClass, "lyr")

        tesRankList = ["Endangered", "Threatened", "Sensitive"]

        for tesRank in tesRankList:
            finalWorkSpace = layerWorkSpace + "\\" + projectedGDB + "\\" + \
                             "EDW_FishWildlife_Observation_2017_" + tesRank[:1]

            arcpy.AddMessage("Selecting records based on " + tesRank + " rank ....")
            arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "GRANK_FIRE = '" + tesRank +"'")
            arcpy.AddMessage("Copying selected records to " + tesRank + " Feature Class ......")
            arcpy.CopyFeatures_management("lyr", finalWorkSpace)


        # finalWorkSpace = layerWorkSpace + "\\" + projectedGDB + "\\" + "EDW_FishWildlife_Observation_2017_E"
        #
        # arcpy.AddMessage("Selecting records based on Endangered rank ....")
        # arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "GRANK_FIRE = 'Endangered'")
        # arcpy.AddMessage("Copying selected records to Endangered Feature Class ......")
        # arcpy.CopyFeatures_management("lyr", finalWorkSpace)
        #
        # finalWorkSpace = layerWorkSpace + "\\" + projectedGDB + "\\" + "EDW_FishWildlife_Observation_2017_T"
        #
        # arcpy.AddMessage("Selecting records based on Threatened rank ....")
        # arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "GRANK_FIRE = 'Threatened'")
        # arcpy.AddMessage("Copying selected records to Threatened Feature Class ......")
        # arcpy.CopyFeatures_management("lyr", finalWorkSpace)
        #
        # finalWorkSpace = layerWorkSpace + "\\" + projectedGDB + "\\" + "EDW_FishWildlife_Observation_2017_S"
        #
        # arcpy.AddMessage("Selecting records based on Sensitive rank ....")
        # arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "GRANK_FIRE = 'Sensitive'")
        # arcpy.AddMessage("Copying selected records to Sensitive Feature Class ......")
        # arcpy.CopyFeatures_management("lyr", finalWorkSpace)

    arcpy.AddMessage("Script complete ... check data and make changes ... then proceed to intersection")

    # -----------------------------------------------------------------------------------
    #  and Note this process will be run in another script within an
    #  ArcGIS Pro environment using PairwiseIntersect_analysis
    # -----------------------------------------------------------------------------------
    # arcpy.Intersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)
    # arcpy.PairwiseIntersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)

    # usfsOwnershipFeatureClass = r"C:\Users\jklaus\Documents\Python_Testing\fire_retardant\USFS_Ownership_LSRS\2017_USFS_Ownership_CAALB83.gdb\USFS_OwnershipLSRS_2017"
    #
    # intersectFeatureClass = outFeatClass + "_intersect"
    #
    # arcpy.AddMessage("Intersecting with USFS Ownership feature class .....")
    # arcpy.AddMessage("Please be patient while this runs .....")

except arcpy.ExecuteError:
    arcpy.GetMessages()
except Exception as e:
    arcpy.AddMessage(e)
