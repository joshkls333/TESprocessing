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

newpath_threatened = in_workspace + "2017_Threatened"
threatened_gdb = "2017_FRA_Threatened_OriginalDataNoBuffers_FWSDeliverable_CAALAB83.gdb"
newpath_endangered = in_workspace + "2017_Endangered"
endangered_gdb = "2017_FRA_Endangered_OriginalDataNoBuffers_FWSDeliverable_CAALAB83.gdb"
newpath_sensitive  = in_workspace + "2017_Sensitive"
sensitive_gdb = "2017_FRA_Sensitive_OriginalDataNoBuffers_FWSDeliverable_CAALAB83.gdb"

if not os.path.exists(newpath_sensitive):
    arcpy.AddMessage("Creating directory for Sensitive Data Deliverables ....")
    os.makedirs(newpath_sensitive)
    arcpy.AddMessage("Creating Geodatabase for Sensitive Data Deliverables ....")
    arcpy.CreateFileGDB_management(newpath_sensitive, sensitive_gdb)

if not os.path.exists(newpath_endangered):
    arcpy.AddMessage("Creating directory for Endangered Data Deliverables ....")
    os.makedirs(newpath_endangered)
    arcpy.AddMessage("Creating Geodatabase for Endangered Data Deliverables ....")
    arcpy.CreateFileGDB_management(newpath_endangered, endangered_gdb)

if not os.path.exists(newpath_threatened):
    arcpy.AddMessage("Creating directory for Threatened Data Deliverables ....")
    os.makedirs(newpath_threatened)
    arcpy.AddMessage("Creating Geodatabase for Threatened Data Deliverables ....")
    arcpy.CreateFileGDB_management(newpath_threatened, threatened_gdb)

# --------------------------------------------------------------------------------
#  Please note the following selections of intable and csv are file dependent
# --------------------------------------------------------------------------------

# intable = sys.argv[2]

# layerType = sys.argv[4]

layerType = "Critical_Habitat_Polygons"

layerWorkSpace = in_workspace + "\\" + layerType + "\\"
projectedGDB = layerType + "_Test_2017_CAALB83_newproj.gdb"
selectFC = layerType + "_2017_Occurrence_found"

arcpy.AddMessage("Layer Type: " + layerType)

#  Need to clean up how to set up workspaces especially if these layers need to be projected
#-------------------------------------------------------------------------------------------

# if intable == "#":
if layerType == "TESP":
    intable = in_workspace + "\\TESP\\EDW_TESP_r05_021617_Everything.gdb\\TESP\\TESP_OccurrenceAll"

#    attempting to make a generic layerworkspace that I can use for all layers
#    layerWorkSpace = in_workspace + "\\" + layerType + "\\"
#    projectedGDB = "Test_2017_TESP_CAALB83_newproj.gdb"
#    selectFC = "EDW_TESP_2017_OccurrenceAll_Found"

elif layerType == "Wildlife_Sites":
    intable = in_workspace + "\\Wildlife\\EDW_FishWildlife_R05_021617_Everything.gdb\\Fish_and_Wildlife\\WildlifeSites"
elif layerType == "Wildlife_Observations":
    intable = in_workspace + "\\Wildlife\\EDW_FishWildlife_R05_021617_Everything.gdb\\Fish_and_Wildlife\\FishWildlife_Observation"
elif layerType == "Critical_Habitat_Polygons":
    # intable = in_workspace + "\\CHab\\2017_CHab_CAALB83.gdb\\CHabPolyAllSelectedSpecies2017_nobuf"
    intable = in_workspace + "\\CHab\\crithab_all_layers\\CRITHAB_POLY.shp"

    # chabWorkSpace = in_workspace + "\\Chab\\crithab_all_layers\\"
    # if arcpy.Exists("Test_Chab_newproj.gdb"):
    #     newspace = chabWorkSpace + "\\Test_Chab_newproj.gdb\\crit_poly_proj"
    # else:
    #     arcpy.CreateFileGDB_management(chabWorkSpace, "Test_Chab_newproj.gdb")
    #     newspace = chabWorkSpace + "\\Test_Chab_newproj.gdb\\crit_poly_proj"
elif layerType == "Critical_Habitat_Lines":
    intable = in_workspace + "\\CHab\\2017_CHab_CAALB83.gdb\\CHabLineAllSelectedSpecies2017"
elif layerType == "CNDDB":
    intable = in_workspace + "\\CNDDB\\gis_gov\\cnddb.shp"

    # cnddbWorkSpace = in_workspace + "\\CNDDB\\"
    # if arcpy.Exists(cnddbWorkSpace + "Test_CNDDB_newproj.gdb"):
    #     newspace = cnddbWorkSpace + "\\Test_CNDDB_newproj.gdb\\CNDDB_2017_All_selects"
    # else:
    #     arcpy.CreateFileGDB_management(cnddbWorkSpace, "Test_CNDDB_newproj.gdb")
    #     newspace = cnddbWorkSpace + "\\Test_CNDDB_newproj.gdb\\CNDDB_2017_All_selects"


#------------------------------------------------------------------------------
# Testing to see if data is projected in NAD 1983 California Teale Albers
# If not run Project_management to project the data
#------------------------------------------------------------------------------

if arcpy.Exists(layerWorkSpace + "\\" + projectedGDB):
    newProjWorkSpace = layerWorkSpace + "\\" + projectedGDB + "\\" + selectFC
else:
    arcpy.CreateFileGDB_management(layerWorkSpace, projectedGDB)
    newProjWorkSpace = layerWorkSpace + "\\" + projectedGDB + "\\" + selectFC


# if layerType == "Critical_Habitat_Polygons" or layerType == "CNDDB":
#     outtable = newspace + "_new"
# else:
#     outtable = intable + "_new"

outtable = newProjWorkSpace + "_newE"

arcpy.AddMessage("Table: " + intable)

spatial_ref = arcpy.Describe(intable).spatialReference

arcpy.AddMessage("Current Spatial Reference is : " + spatial_ref.name)

sr = arcpy.SpatialReference(3310)

if spatial_ref.name != "NAD_1983_California_Teale_Albers":
    arcpy.AddMessage("Reprojecting layer to NAD 1983 California Teale Albers ....")
    arcpy.Project_management(intable, newProjWorkSpace, sr)
#------------------------------------------------------------------------------------------
# Adding fields to store information that will be used for final deliverables
#------------------------------------------------------------------------------------------

arcpy.AddMessage("Adding fields [UnitID, GRANK_FIRE, SOURCEFIRE, SNAME_FIRE, CNAME_FIRE]")
arcpy.AddMessage("Adding fields [BUFFT_FIRE, BUFFM_FIRE, CMNT_FIRE, INST_FIRE]")

arcpy.AddField_management(newProjWorkSpace, "UnitID", "TEXT", "", "", "5", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(newProjWorkSpace, "GRANK_FIRE", "TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(newProjWorkSpace, "SOURCEFIRE", "TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(newProjWorkSpace, "SNAME_FIRE", "TEXT", "", "", "60", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(newProjWorkSpace, "CNAME_FIRE", "TEXT", "", "", "60", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(newProjWorkSpace, "BUFFT_FIRE", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(newProjWorkSpace, "BUFFM_FIRE", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(newProjWorkSpace, "CMNT_FIRE", "TEXT", "", "", "150", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(newProjWorkSpace, "INST_FIRE", "TEXT", "", "", "150", "", "NULLABLE", "NON_REQUIRED", "")


# Note the different ways of bringing in a csv for lookup data on the buffer amount, forest, and status
#_____________________________________________________________________________________________________

# csvFile = sys.argv[3]

# if csvFile == "#":

if layerType == "TESP":
    csvFile = in_workspace + "\\TESP_SummaryTable.csv"
elif layerType == "Wildlife_Sites":
    csvFile = in_workspace + "\\Wildlife_Sites_SummaryTable.csv"
elif layerType == "Wildlife_Observations":
    csvFile = in_workspace + "\\Wildlife_Observations_SummaryTable.csv"
elif layerType == "Critical_Habitat_Polygons":
    csvFile = in_workspace + "\\crithab.csv"
elif layerType == "CNDDB":
    csvFile = in_workspace + "\\CNDDB_SummaryTable.csv"

arcpy.AddMessage("csv File: " + csvFile)

with open(csvFile, 'rb') as f:
    reader = csv.reader(f)
    selectionList = list(reader)

arcpy.AddMessage("Listing of csv table data: ")
for item in selectionList:
    arcpy.AddMessage(item)

if layerType == "TESP":
    sciNameField= "SCIENTIFIC_NAME"
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

# -----------------------------------------------------------------------------------------

try:

    arcpy.MakeFeatureLayer_management(newProjWorkSpace, "lyr" )

    arcpy.AddMessage("-----------------")
    arcpy.AddMessage("Selection: " + selectQuery)
    arcpy.AddMessage("-----------------")

    arcpy.AddMessage("Selecting layers based on selection ....")
    arcpy.SelectLayerByAttribute_management ("lyr", "NEW_SELECTION", selectQuery )

    arcpy.AddMessage("Copying selected records to new feature ......")
    arcpy.CopyFeatures_management("lyr", outtable)

    result = arcpy.GetCount_management(outtable)
    count = int(result.getOutput(0))
    arcpy.AddMessage("Total Number of Records: " + str(count))

    threatNum = 0
    sensitiveNum = 0
    endangerNum = 0
    otherNum = 0
    arcpy.AddMessage("Populating attributes .....")

    if layerType == "Critical_Habitat_Polygons":
        cur = arcpy.UpdateCursor(outtable)

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

            # May delete this if below code captures it:

            # arcpy.AddMessage("Number of Threatened = " + str(threatNum))
            # arcpy.AddMessage("Number of Sensitive = " + str(sensitiveNum))
            # arcpy.AddMessage("Number of Endangered = " + str(endangerNum))

        del cur

    elif layerType == "CNDDB":
        cur = arcpy.UpdateCursor(outtable)
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

            cur.updateRow(row)

        del cur

    else:

        # Need to clean up this code below pull from list instead of csv

        forestField = "FS_UNIT_NAME"
        cur = arcpy.UpdateCursor(outtable)

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



            # Need to clean up this code below pull from list instead of csv

            # with open(csvFile, 'rb') as f:
            #     reader = csv.reader(f)
            #     for line in reader:
            #
            #         species = line[0]
            #         status = line[1]
            #         bufferAmt = line[2]
            #         forest = line[3]
            #
            #         if species.startswith(speciesrow) and forest == "":
            #
            #             if bufferAmt == "NN" or "":
            #                     bufferAmount = 0
            #             else:
            #                     bufferAmount = int(bufferAmt)
            #             break
            #         elif species.startswith(speciesrow) and forest == forestrow:
            #
            #             if bufferAmt == "NN" or "":
            #                     buffer_amount = 0
            #             else:
            #                     buffer_amount = int(bufferAmt)
            #            break



            # if row.getValue(field) in threatenedList :
            #     row.GRANK_FIRE = "Threatened"
            #     threatNum += 1
            # elif row.getValue(field) in sensitiveList:
            #     row.GRANK_FIRE = "Sensitive"
            #     sensitiveNum += 1
            # else:
            #     row.GRANK_FIRE = "Endangered"
            #     endangerNum += 1

            cur.updateRow(row)


        del cur

    arcpy.AddMessage("Number of Threatened = " + str(threatNum))
    arcpy.AddMessage("Number of Sensitive = " + str(sensitiveNum))
    arcpy.AddMessage("Number of Endangered = " + str(endangerNum))
    arcpy.AddMessage("Number of Other = " + str(otherNum))

    arcpy.AddMessage("Splitting current state of data into deliverable Geodatabases .....")

#    does not work in ArcGIS only ArcGIS Pro
#    arcpy.SplitByAttributes_analysis(outtable, sensitive_gdb, "GRANK_FIRE")

#    status_fc = intable + "_noAAAbuf"

#--------------Copying to Sensitive Geodatabase for interim deliverable step
    arcpy.MakeFeatureLayer_management(outtable, "lyr" )

    arcpy.AddMessage("Selecting records based on Sensitive rank ....")
    arcpy.SelectLayerByAttribute_management ("lyr", "NEW_SELECTION", "GRANK_FIRE = 'Sensitive'" )

    if layerType == "TESP":
        outlocation = newpath_sensitive + "\\\\" + sensitive_gdb + "\\\\EDW_TESP_2017_Sensitive_OccurrenceAll_FoundPlants_nobuf"
    elif layerType == "Wildlife_Sites":
        outlocation = newpath_sensitive + "\\\\" + sensitive_gdb + "\\\\EDW_WildlifeSites_2017_Sensitive_nobuf"
    elif layerType == "Wildlife_Observations":
        outlocation = newpath_sensitive + "\\\\" + sensitive_gdb + "\\\\EDW_FishWildlife_Observation_2017_Sensitive_nobuf"
    elif layerType == "Critical_Habitat_Polygons":
        outlocation = newpath_sensitive + "\\\\" + sensitive_gdb + "\\\\CHabPolyAllSelectedSpecies_2017_Sensitive_nobuf"
    elif layerType == "CNDDB":
        outlocation = newpath_sensitive + "\\\\" + sensitive_gdb + "\\\\CNDDB_selects_2017_Sensitive_nobuf"

    arcpy.AddMessage("Copying selected records to Sensitive Geodatabase ......")
    arcpy.CopyFeatures_management("lyr", outlocation)

    result = arcpy.GetCount_management(outlocation)
    count = int(result.getOutput(0))
    arcpy.AddMessage("Total Number of Records: " + str(count))

#--------------Copying to Threatened Geodatabase for interim deliverable step

    arcpy.MakeFeatureLayer_management(outtable, "lyr" )

    arcpy.AddMessage("Selecting records based on Threatened rank ....")
    arcpy.SelectLayerByAttribute_management ("lyr", "NEW_SELECTION", "GRANK_FIRE = 'Threatened'" )

    if layerType == "TESP":
        outlocation = newpath_threatened + "\\\\" + threatened_gdb + "\\\\EDW_TESP_2017_Threatened_OccurrenceAll_FoundPlants_nobuf"
    elif layerType == "Wildlife_Sites":
        outlocation = newpath_threatened + "\\\\" + threatened_gdb + "\\\\EDW_WildlifeSites_2017_Threatened_nobuf"
    elif layerType == "Wildlife_Observations":
        outlocation = newpath_threatened + "\\\\" + threatened_gdb + "\\\\EDW_FishWildlife_Observation_2017_Threatened_nobuf"
    elif layerType == "Critical_Habitat_Polygons":
        outlocation = newpath_threatened + "\\\\" + threatened_gdb + "\\\\CHabPolyAllSelectedSpecies_2017_Threatened_nobuf"
    elif layerType == "CNDDB":
        outlocation = newpath_threatened + "\\\\" + threatened_gdb + "\\\\CNDDB_selects_2017_Threatened_nobuf"

    arcpy.AddMessage("Copying selected records to Threatened Geodatabase ......")
    arcpy.CopyFeatures_management("lyr", outlocation)

    result = arcpy.GetCount_management(outlocation)
    count = int(result.getOutput(0))
    arcpy.AddMessage("Total Number of Threatened Records: " + str(count))

#--------------Copying to Endangered Geodatabase for interim deliverable step
    arcpy.MakeFeatureLayer_management(outtable, "lyr" )

    arcpy.AddMessage("Selecting records based on Endangered rank ....")
    arcpy.SelectLayerByAttribute_management ("lyr", "NEW_SELECTION", "GRANK_FIRE = 'Endangered'" )

    if layerType == "TESP":
        outlocation = newpath_endangered + "\\\\" + endangered_gdb + "\\\\EDW_TESP_2017_Endangered_OccurrenceAll_FoundPlants_nobuf"
    elif layerType == "Wildlife_Sites":
        outlocation = newpath_endangered + "\\\\" + endangered_gdb + "\\\\EDW_WildlifeSites_2017_Endangered_nobuf"
    elif layerType == "Wildlife_Observations":
        outlocation = newpath_endangered + "\\\\" + endangered_gdb + "\\\\EDW_FishWildlife_Observation_2017_Endangered_nobuf"
    elif layerType == "Critical_Habitat_Polygons":
        outlocation = newpath_endangered + "\\\\" + endangered_gdb + "\\\\CHabPolyAllSelectedSpecies_2017_Endangered_nobuf"
    elif layerType == "CNDDB":
        outlocation = newpath_endangered + "\\\\" + endangered_gdb + "\\\\CNDDB_selects_2017_Endangered_nobuf"

    arcpy.AddMessage("Copying selected records to Endangered Geodatabase ......")
    arcpy.CopyFeatures_management("lyr", outlocation)

    result = arcpy.GetCount_management(outlocation)
    count = int(result.getOutput(0))
    arcpy.AddMessage("Total Number of Endangered Records: " + str(count))



#----------------------------------------------------------------------
# Tested below pieces - commenting out to test attribution
#----------------------------------------------------------------------
    outFeatureClass = outtable + "_singlepart"

    arcpy.AddMessage("Converting multipart geometry to singlepart .....")

    arcpy.MultipartToSinglepart_management(outtable, outFeatureClass)

    inCount = int(arcpy.GetCount_management(outtable).getOutput(0))
    outCount = int(arcpy.GetCount_management(outFeatureClass).getOutput(0))

    arcpy.AddMessage("Number of new records: " + str(outCount - inCount))

    arcpy.AddMessage("Repairing Geometry ......")
    arcpy.RepairGeometry_management(outFeatureClass)

    if layerType != "Critcal_Habitat_Polygons":
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
        finalWorkSpace = layerWorkSpace + "\\" + projectedGDB + "\\" + "EDW_FishWildlife_Observation_2017_E"

        arcpy.AddMessage("Selecting records based on Endangered rank ....")
        arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "GRANK_FIRE = 'Endangered'")
        arcpy.AddMessage("Copying selected records to Endangered Feature Class ......")
        arcpy.CopyFeatures_management("lyr", finalWorkSpace)

        finalWorkSpace = layerWorkSpace + "\\" + projectedGDB + "\\" + "EDW_FishWildlife_Observation_2017_T"

        arcpy.AddMessage("Selecting records based on Threatened rank ....")
        arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "GRANK_FIRE = 'Threatened'")
        arcpy.AddMessage("Copying selected records to Threatened Feature Class ......")
        arcpy.CopyFeatures_management("lyr", finalWorkSpace)

        finalWorkSpace = layerWorkSpace + "\\" + projectedGDB + "\\" + "EDW_FishWildlife_Observation_2017_S"

        arcpy.AddMessage("Selecting records based on Sensitive rank ....")
        arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "GRANK_FIRE = 'Sensitive'")
        arcpy.AddMessage("Copying selected records to Sensitive Feature Class ......")
        arcpy.CopyFeatures_management("lyr", finalWorkSpace)



        # usfsOwnershipFeatureClass = r"C:\Users\jklaus\Documents\Python_Testing\fire_retardant\USFS_Ownership_LSRS\2017_USFS_Ownership_CAALB83.gdb\USFS_OwnershipLSRS_2017"
    #
    # intersectFeatureClass = outFeatClass + "_intersect"
    #
    # arcpy.AddMessage("Intersecting with USFS Ownership feature class .....")
    # arcpy.AddMessage("Please be patient while this runs .....")

#-----------------------------------------------------------------------------------

    # Note this process will be run in another script within an ArcGIS Pro environment using PairwiseIntersect_analysis
    # arcpy.Intersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)
    # arcpy.PairwiseIntersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)

except arcpy.ExecuteError:
    arcpy.GetMessages()
except Exception as e:
    arcpy.AddMessage(e)


    # ____________________________________________________________________
    #
    # REMOVED THE BELOW HARDCODED QUERIES AND THREATENED/SENSITIVE LISTS
    #
    #_____________________________________________________________________


    # The following query tl and sl based on TESP
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # selectQuery = """ SCIENTIFIC_NAME = 'Acanthomintha ilicifolia' OR SCIENTIFIC_NAME = 'Acanthoscyphus parishii var. goodmaniana'
    #                   OR SCIENTIFIC_NAME = 'Allium munzii' OR SCIENTIFIC_NAME = 'Allium tribracteatum' OR SCIENTIFIC_NAME = 'Arabis johnstonii'
    #                   OR SCIENTIFIC_NAME = 'Arabis macdonaldiana' OR SCIENTIFIC_NAME = 'Arenaria ursina' OR SCIENTIFIC_NAME = 'Astragalus albens'
    #                   OR SCIENTIFIC_NAME = 'Astragalus brauntonii' OR SCIENTIFIC_NAME = 'Astragalus ertterae' OR SCIENTIFIC_NAME = 'Astragalus pachypus var. jaegeri'
    #                   OR SCIENTIFIC_NAME = 'Astragalus shevockii' OR SCIENTIFIC_NAME = 'Astragalus tricarinatus' OR SCIENTIFIC_NAME = 'Baccharis vanessae'
    #                   OR SCIENTIFIC_NAME = 'Berberis nevinii' OR SCIENTIFIC_NAME = 'Brodiaea filifolia' OR SCIENTIFIC_NAME = 'Castilleja cinerea'
    #                   OR SCIENTIFIC_NAME = 'Castilleja plagiotoma' OR SCIENTIFIC_NAME = 'Caulanthus californicus' OR SCIENTIFIC_NAME = 'Ceanothus ophiochilus'
    #                   OR SCIENTIFIC_NAME = 'Chorizanthe parryi var. parryi' OR SCIENTIFIC_NAME = 'Chorizanthe polygonoides ssp. longispina'
    #                   OR SCIENTIFIC_NAME = 'Clarkia springvillensis' OR SCIENTIFIC_NAME = 'Delphinium hesperium ssp. cuyamacae'
    #                   OR SCIENTIFIC_NAME = 'Dicentra nevadensis' OR SCIENTIFIC_NAME = 'Dodecahema leptoceras' OR SCIENTIFIC_NAME = 'Erigeron parishii'
    #                   OR SCIENTIFIC_NAME = 'Eriogonum breedlovei var. breedlovei' OR SCIENTIFIC_NAME = 'Eriogonum kennedyi var. austromontanum'
    #                   OR SCIENTIFIC_NAME = 'Eriogonum ovalifolium var. vineum' OR SCIENTIFIC_NAME = 'Eriogonum spectabile' OR SCIENTIFIC_NAME = 'Horkelia tularensis'
    #                   OR SCIENTIFIC_NAME = 'Imperata brevifolia' OR SCIENTIFIC_NAME = 'Leptosiphon floribundum ssp. hallii' OR SCIENTIFIC_NAME = 'Lupinus constancei'
    #                   OR SCIENTIFIC_NAME = 'Monardella macrantha ssp. hallii' OR SCIENTIFIC_NAME = 'Monardella viridis ssp. saxicola'
    #                   OR SCIENTIFIC_NAME = 'Nemacladus twisselmannii' OR SCIENTIFIC_NAME = 'Orcuttia tenuis' OR SCIENTIFIC_NAME = 'Oreonana vestita'
    #                   OR SCIENTIFIC_NAME = 'Penstemon californicus' OR SCIENTIFIC_NAME = 'Phlox hirsuta' OR SCIENTIFIC_NAME = 'Physaria kingii ssp. bernardina'
    #                   OR SCIENTIFIC_NAME = 'Lesquerella kingii ssp. bernardina' OR SCIENTIFIC_NAME = 'Poa atropurpurea' OR SCIENTIFIC_NAME = 'Pseudobahia peirsonii'
    #                   OR SCIENTIFIC_NAME = 'Packera layneae' OR SCIENTIFIC_NAME = 'Sidalcea hickmanii ssp. parishii' OR SCIENTIFIC_NAME = 'Sidalcea keckii'
    #                   OR SCIENTIFIC_NAME = 'Sidalcea pedata' OR SCIENTIFIC_NAME = 'Streptanthus cordatus var. piutensis' OR SCIENTIFIC_NAME = 'Streptanthus fenestratus'
    #                   OR SCIENTIFIC_NAME = 'Taraxacum californicum' OR SCIENTIFIC_NAME = 'Thelypodium stenopetalum' OR SCIENTIFIC_NAME = 'Thelypteris puberula var. sonorensis'
    #                   OR SCIENTIFIC_NAME = 'Trifolium dedeckerae' OR SCIENTIFIC_NAME = 'Tuctoria greenei' OR SCIENTIFIC_NAME = 'Howellia aquatilis'
    #                   OR SCIENTIFIC_NAME = 'Heterotheca shevockii' OR SCIENTIFIC_NAME = 'Marina orcuttii var. orcuttii'
    #                   OR ACCEPTED_SCIENTIFIC_NAME = 'Mahonia nevinii' OR ACCEPTED_SCIENTIFIC_NAME = 'Stanfordia californica' OR ACCEPTED_SCIENTIFIC_NAME = 'Clarkia springvillensis'
    #                   OR ACCEPTED_SCIENTIFIC_NAME = 'Abronia alpina' OR ACCEPTED_SCIENTIFIC_NAME = 'Calochortus persistens' """
    #
    #
    #
    # tl = """Acanthomintha ilicifolia,Arenaria ursina,Astragalus tricarinatus,
    #         Baccharis vanessae,Brodiaea filifolia,
    #         Castilleja cinerea,Ceanothus ophiochilus,Eriogonum kennedyi var. austromontanum,
    #         Orcuttia tenuis,Pseudobahia peirsonii,Howellia aquatilis"""
    #
    #
    # sl = """Allium tribracteatum,Arabis johnstonii,Astragalus ertterae,Astragalus pachypus var. jaegeri,Astragalus shevockii,Castilleja plagiotoma,
    #         Chorizanthe parryi var. parryi,Chorizanthe polygonoides ssp. longispina,Delphinium hesperium ssp. cuyamacae,Dicentra nevadensis,
    #         riogonum breedlovei var. breedlovei,Eriogonum spectabile,Lupinus constancei,Monardella macrantha ssp. hallii,
    #         Monardella viridis ssp. saxicola,Nemacladus twisselmannii,Oreonana vestita,Penstemon californicus,Streptanthus cordatus var. piutensis,
    #         Streptanthus fenestratus,Thelypteris puberula var. sonorensis,Trifolium dedeckerae,Sidalcea hickmanii ssp. parishii,Heterotheca shevockii,
    #         Horkelia tularensis, Marina orcuttii var. orcuttii"""

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # The following query tl and sl based on Wildlife Sites
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #
    # selectQuery = """
    #                 SCI_NAME = 'Bufo canorus' OR SCI_NAME = 'Bufo californicus' OR SCI_NAME = 'Dipodomys stephensi'
    #              OR SCI_NAME = 'Empidonax traillii extimus' OR SCI_NAME = 'Euphydryas editha quino' OR SCI_NAME = 'Lycaena hermes'
    #              OR SCI_NAME = 'Pyrgus ruralis lagunae' OR SCI_NAME = 'Rana aurora draytonii' OR SCI_NAME = 'Rana draytonii'
    #              OR SCI_NAME = 'Rana muscosa' OR SCI_NAME = 'Rana sierrae' OR SCI_NAME = 'Vireo bellii pusillus' OR SCI_NAME = 'Polioptila californica'
    #              OR SCI_NAME = 'Anaxyrus californicus' OR SCI_NAME = 'Bufo microscaphus californicus'
    #             """
    #
    #
    #
    # tl = "Bufo canorus,Rana aurora draytonii,Rana draytonii"
    #
    #
    # sl = "Lycaena hermes"

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # The following query tl and sl based on Wildlife Observations
    # #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #
    # selectQuery = """
    #                 SCIENTIFIC_NAME = 'Bufo californicus' OR SCIENTIFIC_NAME = 'Anaxyrus californicus' OR SCIENTIFIC_NAME = 'Gambelia sila'
    #             OR SCIENTIFIC_NAME = 'Gymnogyps californianus' OR SCIENTIFIC_NAME = 'Polioptila californica californica'
    #             OR SCIENTIFIC_NAME = 'Rana draytonii' OR SCIENTIFIC_NAME = 'Rana aurora draytonii' OR SCIENTIFIC_NAME = 'Ambystoma californiense'
    #             OR SCIENTIFIC_NAME = 'Acipenser medirostris' OR SCIENTIFIC_NAME = 'Lycaena hermes' OR SCIENTIFIC_NAME = 'Pyrgus ruralis lagunae'
    #             OR SCIENTIFIC_NAME = 'Oncorhynchus clarkii henshawi' OR SCIENTIFIC_NAME = 'Vireo bellii pusillus' OR SCIENTIFIC_NAME = 'Rana muscosa'
    #             OR SCIENTIFIC_NAME = 'Thaleichthys pacificus' OR SCIENTIFIC_NAME = 'Oncorhynchus clarkii seleniris' OR SCIENTIFIC_NAME = 'Euphydryas editha quino'
    #             OR SCIENTIFIC_NAME = 'Dipodomys merriami parvus' OR SCIENTIFIC_NAME = 'Catostomus santaanae' OR SCIENTIFIC_NAME = 'Pacifastacus fortis'
    #             OR SCIENTIFIC_NAME = 'Rana sierrae' OR SCIENTIFIC_NAME = 'Oncorhynchus kisutch' OR SCIENTIFIC_NAME = 'Empidonax traillii extimus'
    #             OR SCIENTIFIC_NAME = 'Dipodomys stephensi' OR SCIENTIFIC_NAME = 'Branchinecta lynchi' OR SCIENTIFIC_NAME = 'Lepidurus packardi'
    #             OR SCIENTIFIC_NAME = 'Coccyzus americanus occidentalis' OR SCIENTIFIC_NAME = 'Bufo canorus' OR SCIENTIFIC_NAME = 'Anaxyrus canorus'
    #             OR SCIENTIFIC_NAME = 'Polioptila californica' OR SCIENTIFIC_NAME = 'Gasterosteus aculeatus williamsoni'
    #             """
    #
    #             #  Please note:  Need to do special selection for COMMON_NAME = "Foothill Yellow-legged Frog" or "Mountain Yellow-legged Frog"
    #
    # tl = "Acipenser medirostris,Ambystoma californiense,Anaxyrus canorus,Branchinecta lynchi,Bufo canorus,Oncorhynchus clarkii henshawi,Oncorhynchus clarkii seleniris,Oncorhynchus kisutch"
    #
    #
    # sl = "Lycaena hermes"

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
