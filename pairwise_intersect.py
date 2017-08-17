# pairwise_intersect.py
#
# Usage: PairwiseIntersect_analysis
# Description: Performs an Intersect_analysis with pairwise processing that only
#              runs in ArcGIS Pro. After I drop unnecessary fields and perform a repair geometry.
# Created by: Josh Klaus 08/01/2017
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import sys
import csv

# in_workspace = sys.argv[1]

in_workspace = "C:\\Users\\jklaus\\Documents\\Python_Testing\\fire_retardant\\"
local_gdb = "C:\\Users\\jklaus\\Documents\\Python_Testing\\fire_retardant\\Local_Data\\2017_Local_CAALB83.gdb\\"
local_data = local_gdb + "\\Explode"

layerType = "TESP"

# layerType = sys.argv[2]

sr = arcpy.SpatialReference(3310)

if layerType == "Local":
    arcpy.env.workspace = local_data
    if arcpy.Exists(local_gdb + "\\Intersect_New"):
        intersectFeatureDataset = local_gdb + "\\Intersect_New\\"
    else:
        arcpy.CreateFeatureDataset_management(local_gdb, "Intersect_New", 3310)
        intersectFeatureDataset = local_gdb + "\\Intersect_New\\"
else:
    arcpy.env.workspace = in_workspace

arcpy.env.overwriteOutput = True

# intable = r"C:\Users\jklaus\Documents\Python_Testing\fire_retardant\2017_EDW_CAALB83.gdb\EDW_TESP_2017_OccurrenceAll_FoundPlants_newH_"

# outFeatClass = in_workspace + "\\" + layerType + "\\Critical_Habitat_Polygons_Test_2017_CAALB83_newproj.gdb\Critical_Habitat_Polygons_2017_Occurrence_found_newE_singlepart"

outFeatClass = in_workspace + "\\" + layerType + "\\TESP_Test_2017_CAALB83_newproj.gdb\\TESP_2017_Occurrence_found_newE_singlepart_buffer_spart"

# outFeatClass = sys.argv[1]

newpath_threatened = in_workspace + "2017_Threatened"
newpath_endangered = in_workspace + "2017_Endangered"
newpath_sensitive  = in_workspace + "2017_Sensitive"

threatened_gdb = "2017_Threatened_IdentInter_CAALAB83.gdb"
endangered_gdb = "2017_Endangered_IdentInter_CAALAB83.gdb"
sensitive_gdb  = "2017_Sensitive_IdentInter_CAALAB83.gdb"

fra_threatened_gdb = "2017_FRA_Threatened_OriginalDataBufferedAndNonBufferedAreas_CAALAB83.gdb"
fra_endangered_gdb = "2017_FRA_Endangered_OriginalDataBufferedAndNonBufferedAreas_CAALAB83.gdb"
fra_sensitive_gdb  = "2017_FRA_Sensitive_OriginalDataBufferedAndNonBufferedAreas_CAALAB83.gdb"

if arcpy.Exists(newpath_threatened + "\\" + threatened_gdb):
    arcpy.AddMessage("Threatened GDB exists")
else:
    arcpy.AddMessage("Creating Geodatabase for Sensitive Data Deliverables containing intersection data ....")
    arcpy.CreateFileGDB_management(newpath_sensitive, sensitive_gdb)
    arcpy.CreateFileGDB_management(newpath_sensitive, fra_sensitive_gdb)

if arcpy.Exists(newpath_endangered + "\\" + endangered_gdb):
    arcpy.AddMessage("Endangered GDB exists")
else:
    arcpy.AddMessage("Creating Geodatabase for Endangered Data Deliverables containing intersection data ....")
    arcpy.CreateFileGDB_management(newpath_endangered, endangered_gdb)
    arcpy.CreateFileGDB_management(newpath_endangered, fra_endangered_gdb)

if arcpy.Exists(newpath_sensitive + "\\" + sensitive_gdb):
    arcpy.AddMessage("Sensitive GDB exists")
else:
    arcpy.AddMessage("Creating Geodatabase for Threatened Data Deliverables containing intersection data ....")
    arcpy.CreateFileGDB_management(newpath_threatened, threatened_gdb)
    arcpy.CreateFileGDB_management(newpath_threatened, fra_threatened_gdb)


def copy_to_final_gdb(filename):

    # --------------Copying to Sensitive Geodatabase for interim deliverable step

    arcpy.MakeFeatureLayer_management(dissolveFeatureClass, "tmplyr")

    arcpy.AddMessage("Selecting records based on Sensitive rank ....")
    arcpy.SelectLayerByAttribute_management("tmplyr", "NEW_SELECTION", "GRANK_FIRE = 'Sensitive'")
    finalLocation = ""
    arcpy.AddMessage("testing...." + finalLocation)

    finalLocation = newpath_sensitive + "\\" + sensitive_gdb + "\\"

    if layerType == "TESP":
        finalLocation += "EDW_TESP_2017_Sensitive_OccurrenceAll_FoundPlants_nobuf"
    elif layerType == "Wildlife_Sites":
        finalLocation += "EDW_WildlifeSites_2017_Sensitive_nobuf"
    elif layerType == "Wildlife_Observations":
        finalLocation += "EDW_FishWildlife_Observation_2017_Sensitive_nobuf"
    elif layerType == "Critical_Habitat_Polygons":
        finalLocation += "CHabPolyAllSelectedSpecies_2017_Sensitive_nobuf"
    elif layerType == "CNDDB":
        finalLocation += "CNDDB_selects_2017_Sensitive_nobuf"
    elif layerType == "Local":
        finalLocation += filename

    result = arcpy.GetCount_management("tmplyr")
    count = int(result.getOutput(0))
    arcpy.AddMessage("Total Number of Records: " + str(count))

    if count > 0:
        arcpy.AddMessage("Copying selected records to Final Stage Sensitive Geodatabase ......")
        arcpy.CopyFeatures_management("tmplyr", finalLocation)

    # --------------Copying to Threatened Geodatabase for interim deliverable step

    arcpy.MakeFeatureLayer_management(dissolveFeatureClass, "tmplyr")

    arcpy.AddMessage("Selecting records based on Threatened rank ....")
    arcpy.SelectLayerByAttribute_management("tmplyr", "NEW_SELECTION", "GRANK_FIRE = 'Threatened'")

    finalLocation = newpath_threatened + "\\" + threatened_gdb + "\\"

    if layerType == "TESP":
        finalLocation += "EDW_TESP_2017_Threatened_OccurrenceAll_FoundPlants_nobuf"
    elif layerType == "Wildlife_Sites":
        finalLocation += "EDW_WildlifeSites_2017_Threatened_nobuf"
    elif layerType == "Wildlife_Observations":
        finalLocation += "EDW_FishWildlife_Observation_2017_Threatened_nobuf"
    elif layerType == "Critical_Habitat_Polygons":
        finalLocation += "CHabPolyAllSelectedSpecies_2017_Threatened_nobuf"
    elif layerType == "CNDDB":
        finalLocation += "CNDDB_selects_2017_Threatened_nobuf"
    elif layerType == "Local":
        finalLocation += filename

    result = arcpy.GetCount_management("tmplyr")
    count = int(result.getOutput(0))
    arcpy.AddMessage("Total Number of Records: " + str(count))

    if count > 0:
        arcpy.AddMessage("Copying selected records to Final Stage Threatened Geodatabase ......")
        arcpy.CopyFeatures_management("tmplyr", finalLocation)

    # --------------Copying to Endangered Geodatabase for interim deliverable step

    arcpy.MakeFeatureLayer_management(dissolveFeatureClass, "tmplyr")

    arcpy.AddMessage("Selecting records based on Endangered rank ....")
    arcpy.SelectLayerByAttribute_management("tmplyr", "NEW_SELECTION", "GRANK_FIRE = 'Endangered'")

    finalLocation = newpath_endangered + "\\" + endangered_gdb + "\\"

    if layerType == "TESP":
        finalLocation += "EDW_TESP_2017_Endangered_OccurrenceAll_FoundPlants_nobuf"
    elif layerType == "Wildlife_Sites":
        finalLocation += "EDW_WildlifeSites_2017_Endangered_nobuf"
    elif layerType == "Wildlife_Observations":
        finalLocation += "EDW_FishWildlife_Observation_2017_Endangered_nobuf"
    elif layerType == "Critical_Habitat_Polygons":
        finalLocation += "CHabPolyAllSelectedSpecies_2017_Endangered_nobuf"
    elif layerType == "CNDDB":
        finalLocation += "CNDDB_selects_2017_Endangered_nobuf"
    elif layerType == "Local":
        finalLocation += filename

    result = arcpy.GetCount_management("tmplyr")
    count = int(result.getOutput(0))
    arcpy.AddMessage("Total Number of Records: " + str(count))

    if count > 0:
        arcpy.AddMessage("Copying selected records to Final Stage Endangered Geodatabase ......")
        arcpy.CopyFeatures_management("tmplyr", finalLocation)

    arcpy.AddMessage("Complete copying data to final staging GDB")
    return


def copy_to_interim_gdb(filename):

    # --------------Copying to Sensitive Geodatabase for interim deliverable step

    arcpy.MakeFeatureLayer_management(intersectFeatureClass, "lyr")

    arcpy.AddMessage("Selecting records based on Sensitive rank ....")
    arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "GRANK_FIRE = 'Sensitive'")

    outlocation = newpath_sensitive + "\\" + fra_sensitive_gdb + "\\"

    if layerType == "TESP":
        outlocation += "EDW_TESP_2017_OccurrenceAll_FoundPlants_ident_Sensitive"
    elif layerType == "Wildlife_Sites":
        outlocation += "EDW_WildlifeSites_2017_ident_Sensitive"
    elif layerType == "Wildlife_Observations":
        outlocation += "EDW_FishWildlife_Observation_2017_S_ident"
    elif layerType == "Critical_Habitat_Polygons":
        outlocation += "CHabPolyAllSelectedSpecies_2017_nobuf_Ident_Sensitive"
    elif layerType == "CNDDB":
        outlocation += "CNDDB_2017_All_selectsAndShastaCrayfish_Ident_noBDF_Sensitive_nobuf"
    elif layerType == "Local":
        outlocation += filename

    result = arcpy.GetCount_management("lyr")
    count = int(result.getOutput(0))
    arcpy.AddMessage("Total Number of Records: " + str(count))

    if count >0:
        arcpy.AddMessage("Copying selected records to Sensitive Geodatabase ......")
        arcpy.CopyFeatures_management("lyr", outlocation)

    # --------------Copying to Threatened Geodatabase for interim deliverable step

    arcpy.MakeFeatureLayer_management(intersectFeatureClass, "lyr")

    arcpy.AddMessage("Selecting records based on Threatened rank ....")
    arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "GRANK_FIRE = 'Threatened'")

    outlocation = newpath_threatened + "\\" + fra_threatened_gdb + "\\"

    if layerType == "TESP":
        outlocation += "EDW_TESP_2017_OccurrenceAll_FoundPlants_ident_Threatened"
    elif layerType == "Wildlife_Sites":
        outlocation += "EDW_WildlifeSites_2017_ident_Threatened"
    elif layerType == "Wildlife_Observations":
        outlocation += "EDW_FishWildlife_Observation_2017_T_ident"
    elif layerType == "Critical_Habitat_Polygons":
        outlocation += "CHabPolyAllSelectedSpecies_2017_nobuf_Ident_Threatened"
    elif layerType == "CNDDB":
        outlocation += "CNDDB_2017_All_selectsAndShastaCrayfish_Ident_noBDF_Threatened_nobuf"
    elif layerType == "Local":
        outlocation += filename

    result = arcpy.GetCount_management("lyr")
    count = int(result.getOutput(0))
    arcpy.AddMessage("Total Number of Records: " + str(count))

    if count > 0:
        arcpy.AddMessage("Copying selected records to Threatened Geodatabase ......")
        arcpy.CopyFeatures_management("lyr", outlocation)

    # --------------Copying to Endangered Geodatabase for interim deliverable step

    arcpy.MakeFeatureLayer_management(intersectFeatureClass, "lyr")

    arcpy.AddMessage("Selecting records based on Endangered rank ....")
    arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "GRANK_FIRE = 'Endangered'")

    outlocation = newpath_endangered + "\\" + fra_endangered_gdb + "\\"

    if layerType == "TESP":
        outlocation += "EDW_TESP_2017_OccurrenceAll_FoundPlants_ident_Endangered"
    elif layerType == "Wildlife_Sites":
        outlocation += "EDW_WildlifeSites_2017_ident_Endangered"
    elif layerType == "Wildlife_Observations":
        outlocation += "EDW_FishWildlife_Observation_2017_E_ident"
    elif layerType == "Critical_Habitat_Polygons":
        outlocation += "CHabPolyAllSelectedSpecies_2017_nobuf_Ident_Endangered"
    elif layerType == "CNDDB":
        outlocation += "CNDDB_2017_All_selectsAndShastaCrayfish_Ident_noBDF_Endangered_nobuf"
    elif layerType == "Local":
        outlocation += filename

    result = arcpy.GetCount_management("lyr")
    count = int(result.getOutput(0))
    arcpy.AddMessage("Total Number of Records: " + str(count))

    if count > 0:
        arcpy.AddMessage("Copying selected records to Endangered Geodatabase ......")
        arcpy.CopyFeatures_management("lyr", outlocation)

    arcpy.AddMessage("Complete copying data to interim deliverable GDB for Fish and Wildlife")
    return


def unitid_dissolve(filename):

    arcpy.AddMessage("Updating UnitID field from intersection")

    cur = arcpy.UpdateCursor(filename)

    field = "UnitID_FS"

    # populating UnitID field with UnitID_FS field
    for row in cur:
        row.UnitID = "0" + str(row.getValue(field))
        cur.updateRow(row)

    del cur

    arcpy.AddMessage("testing ....")

    # Not needed since Dissolve removes all unnecessary fields

    # Set local variables
    # inFeatures = intersectFeatureClass
    # outFeatureClass = intersectFeatureClass + "_noFields"
    # featureIDfield = "FID_" + outFeatureClass
    # dropFields = ["EO_NUMBER", "ACCEPTED_PLANT_CODE", "NRCS_PLANT_CODE","LIFEFORM","DATE_COLLECTED",
    #               "DATE_COLLECTED_MOST_RECENT", "CURRENT_MEASUREMENT", "AREA_OCCUPENCY" ,
    #               "PLANT_COUNT", "PLANT_COUNT_TYPE" , "ECOLOGICAL_TYPE", "COVER_PCT",
    #               "COVER_CLASS_SET_NAME","COVER_CLASS_CODE","SPECIES_LIST_COMPLETENESS","QUALITY_CONTROL",
    #               "LOCATIONAL_UNCERTAINTY","SLOPE","ASPECT_AZIMUTH","ASPECT_CARDINAL","ELEVATION_AVERAGE",
    #               "EXISTING_VEG_CLASS","POTENTIAL_VEG_CLASS","OWNER_NAME","FS_UNIT_NAME","SOURCE_GEOMETRY_TYPE",
    #               "FEATURE_CN","EO_CN","SPATIAL_ID","LAST_UPDATE","PLANT_FOUND","GIS_ACRES","GIS_MILES","EXAMINERS",
    #               "BASICOWNERSHIPID", "OWNERCLASSIFICATION", "GIS_ACRES_1", "REGION", "FORESTNAME", "AREA_OCCUPANCY",
    #               "SCIENTIFIC_NAME", "ACCEPTED_SCIENTIFIC_NAME", "COMMON_NAME", "ACCEPTED_COMMON_NAME",
    #               "ORIG_FID", "FID_USFS_OwnershipLSRS_2017", "REGION_1", "SITE_ID_FS",
    #               "FS_UNIT_ID","FORESTNAME_1", "UnitID_FS", featureIDfield]
    #
    # # Execute CopyFeatures to make a new copy of the feature class
    # #  Use CopyRows if you have a table
    # arcpy.CopyFeatures_management(inFeatures, outFeatureClass)
    #
    # arcpy.AddMessage("Deleting all unnecessary fields ......")
    # # Execute DeleteField
    # arcpy.DeleteField_management(outFeatureClass, dropFields)

    arcpy.AddMessage("Repairing Geometry ......")
    arcpy.RepairGeometry_management(filename)

    arcpy.AddMessage("Dissolving Features")

    dissolveFeatureClass = filename + "_dissolved"

    # arcpy.PairwiseDissolve_analysis(intersectFeatureClass, dissolveFeatureClass,
    #                           ["UnitID", "GRANK_FIRE", "SNAME_FIRE", "CNAME_FIRE", "SOURCEFIRE",
    #                            "BUFFT_FIRE", "BUFFM_FIRE", "CMNT_FIRE", "INST_FIRE"])

    arcpy.Dissolve_management(filename, dissolveFeatureClass,
                                    ["UnitID", "GRANK_FIRE", "SNAME_FIRE", "CNAME_FIRE", "SOURCEFIRE",
                                     "BUFFT_FIRE", "BUFFM_FIRE", "CMNT_FIRE", "INST_FIRE"],"","SINGLE_PART")

    # May delete this once I confirm we don't need BUFF_DIST from Stacey
    # arcpy.PairwiseDissolve_analysis(intersectFeatureClass, dissolveFeatureClass,
    #                                 ["UnitID", "GRANK_FIRE", "SNAME_FIRE", "CNAME_FIRE", "SOURCEFIRE",
    #                                  "BUFFT_FIRE", "BUFFM_FIRE", "CMNT_FIRE", "INST_FIRE", "BUFF_DIST"])

    arcpy.AddMessage("Repairing Dissolved Geometry ......")
    arcpy.RepairGeometry_management(filename)
    arcpy.AddMessage("Dissolve and Repair complete")


    return dissolveFeatureClass


try:

    if layerType == "Local":
        fcList = arcpy.ListFeatureClasses()

        for fc in fcList:
            arcpy.AddMessage("--------------------------------------------------")
            arcpy.AddMessage("Intersecting " + fc)
            outFeatClass = fc

            usfsOwnershipFeatureClass = in_workspace + "\\USFS_Ownership_LSRS\\2017_USFS_Ownership_CAALB83.gdb\\USFS_OwnershipLSRS_2017"

            intersectFeature = outFeatClass + "_intersect"

            arcpy.AddMessage("Intersecting with USFS Ownership feature class .....")
            arcpy.AddMessage("Please be patient while this runs .....")

            intersectFeatureClass = intersectFeatureDataset + "\\" + intersectFeature

            arcpy.Intersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)

            # arcpy.PairwiseIntersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)

            copy_to_interim_gdb(fc)

            dissolveFeatureClass = unitid_dissolve(intersectFeatureClass)

            copy_to_final_gdb(fc)
    else:

        usfsOwnershipFeatureClass = in_workspace + "\\USFS_Ownership_LSRS\\2017_USFS_Ownership_CAALB83.gdb\\USFS_OwnershipLSRS_2017"

        intersectFeatureClass = outFeatClass + "_intersect"

        arcpy.AddMessage("Intersecting with USFS Ownership feature class .....")
        arcpy.AddMessage("Please be patient while this runs .....")

        arcpy.Intersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)

        # arcpy.PairwiseIntersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)

        arcpy.AddMessage("Completed Intersection")

        copy_to_interim_gdb(layerType)

        dissolveFeatureClass = unitid_dissolve(intersectFeatureClass)

        copy_to_final_gdb(layerType)

    arcpy.AddMessage("Completed Script successfully!!")

except arcpy.ExecuteError:
    arcpy.GetMessages()
except Exception as e:
    arcpy.AddMessage(e)


