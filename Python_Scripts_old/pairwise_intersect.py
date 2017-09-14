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

arcpy.env.workspace = in_workspace
arcpy.env.overwriteOutput = True

# intable = r"C:\Users\jklaus\Documents\Python_Testing\fire_retardant\2017_EDW_CAALB83.gdb\EDW_TESP_2017_OccurrenceAll_FoundPlants_newH_"

layerType = "TESP"

# layerType = sys.argv[2]

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

outlocation = ""

if arcpy.Exists(threatened_gdb):
    arcpy.AddMessage("Threatened GDB exists")
else:
    arcpy.AddMessage("Creating Geodatabase for Sensitive Data Deliverables containing intersection data ....")
    arcpy.CreateFileGDB_management(newpath_sensitive, sensitive_gdb)
    arcpy.CreateFileGDB_management(newpath_sensitive, fra_sensitive_gdb)

if arcpy.Exists(endangered_gdb):
    arcpy.AddMessage("Endangered GDB exists")
else:
    arcpy.AddMessage("Creating Geodatabase for Endangered Data Deliverables containing intersection data ....")
    arcpy.CreateFileGDB_management(newpath_endangered, endangered_gdb)
    arcpy.CreateFileGDB_management(newpath_endangered, fra_endangered_gdb)

if arcpy.Exists(sensitive_gdb):
    arcpy.AddMessage("Sensitive GDB exists")
else:
    arcpy.AddMessage("Creating Geodatabase for Threatened Data Deliverables containing intersection data ....")
    arcpy.CreateFileGDB_management(newpath_threatened, threatened_gdb)
    arcpy.CreateFileGDB_management(newpath_threatened, fra_threatened_gdb)

try:
    usfsOwnershipFeatureClass = r"C:\Users\jklaus\Documents\Python_Testing\fire_retardant\USFS_Ownership_LSRS\2017_USFS_Ownership_CAALB83.gdb\USFS_OwnershipLSRS_2017"

    intersectFeatureClass = outFeatClass + "_intersect"

    arcpy.AddMessage("Intersecting with USFS Ownership feature class .....")
    arcpy.AddMessage("Please be patient while this runs .....")
    # arcpy.Intersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)
    arcpy.PairwiseIntersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)

    # --------------Copying to Sensitive Geodatabase for interim deliverable step
    arcpy.MakeFeatureLayer_management(outFeatureClass, "lyr")

    arcpy.AddMessage("Selecting records based on Sensitive rank ....")
    arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "GRANK_FIRE = 'Sensitive'")

    if layerType == "TESP":
        outlocation = newpath_sensitive + "\\\\" + fra_sensitive_gdb + "\\\\EDW_TESP_2017_OccurrenceAll_FoundPlants_ident_Sensitive"
    elif layerType == "Wildlife_Sites":
        outlocation = newpath_sensitive + "\\\\" + fra_sensitive_gdb + "\\\\EDW_WildlifeSites_2017_ident_Sensitive"
    elif layerType == "Wildlife_Observations":
        outlocation = newpath_sensitive + "\\\\" + fra_sensitive_gdb + "\\\\EDW_FishWildlife_Observation_2017_S_ident"
    elif layerType == "Critical_Habitat_Polygons":
        outlocation = newpath_sensitive + "\\\\" + fra_sensitive_gdb + "\\\\CHabPolyAllSelectedSpecies_2017_nobuf_Ident_Sensitive"
    elif layerType == "CNDDB":
        outlocation = newpath_sensitive + "\\\\" + fra_sensitive_gdb + "\\\\CNDDB_2017_All_selectsAndShastaCrayfish_Ident_noBDF_Sensitive_nobuf"

    arcpy.AddMessage("Copying selected records to Sensitive Geodatabase ......")
    arcpy.CopyFeatures_management("lyr", outlocation)

    result = arcpy.GetCount_management(outlocation)
    count = int(result.getOutput(0))
    arcpy.AddMessage("Total Number of Records: " + str(count))

    # --------------Copying to Threatened Geodatabase for interim deliverable step

    arcpy.MakeFeatureLayer_management(outFeatureClass, "lyr")

    arcpy.AddMessage("Selecting records based on Threatened rank ....")
    arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "GRANK_FIRE = 'Threatened'")

    if layerType == "TESP":
        outlocation = newpath_threatened + "\\\\" + fra_threatened_gdb + "\\\\EDW_TESP_2017_OccurrenceAll_FoundPlants_ident_Threatened"
    elif layerType == "Wildlife_Sites":
        outlocation = newpath_threatened + "\\\\" + fra_threatened_gdb + "\\\\EDW_WildlifeSites_2017_ident_Threatened"
    elif layerType == "Wildlife_Observations":
        outlocation = newpath_threatened + "\\\\" + fra_threatened_gdb + "\\\\EDW_FishWildlife_Observation_2017_T_ident"
    elif layerType == "Critical_Habitat_Polygons":
        outlocation = newpath_threatened + "\\\\" + fra_threatened_gdb + "\\\\CHabPolyAllSelectedSpecies_2017_nobuf_Ident_Threatened"
    elif layerType == "CNDDB":
        outlocation = newpath_threatened + "\\\\" + fra_threatened_gdb + "\\\\CNDDB_2017_All_selectsAndShastaCrayfish_Ident_noBDF_Threatened_nobuf"

    arcpy.AddMessage("Copying selected records to Threatened Geodatabase ......")
    arcpy.CopyFeatures_management("lyr", outlocation)

    result = arcpy.GetCount_management(outlocation)
    count = int(result.getOutput(0))
    arcpy.AddMessage("Total Number of Threatened Records: " + str(count))

    # --------------Copying to Endangered Geodatabase for interim deliverable step
    arcpy.MakeFeatureLayer_management(outFeatureClass, "lyr")

    arcpy.AddMessage("Selecting records based on Endangered rank ....")
    arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "GRANK_FIRE = 'Endangered'")

    if layerType == "TESP":
        outlocation = newpath_endangered + "\\\\" + fra_endangered_gdb + "\\\\EDW_TESP_2017_OccurrenceAll_FoundPlants_ident_Endangered"
    elif layerType == "Wildlife_Sites":
        outlocation = newpath_endangered + "\\\\" + fra_endangered_gdb + "\\\\EDW_WildlifeSites_2017_ident_Endangered"
    elif layerType == "Wildlife_Observations":
        outlocation = newpath_endangered + "\\\\" + fra_endangered_gdb + "\\\\EDW_FishWildlife_Observation_2017_E_ident"
    elif layerType == "Critical_Habitat_Polygons":
        outlocation = newpath_endangered + "\\\\" + fra_endangered_gdb + "\\\\CHabPolyAllSelectedSpecies_2017_nobuf_Ident_Endangered"
    elif layerType == "CNDDB":
        outlocation = newpath_endangered + "\\\\" + fra_endangered_gdb + "\\\\CNDDB_2017_All_selectsAndShastaCrayfish_Ident_noBDF_Endangered_nobuf"

    arcpy.AddMessage("Copying selected records to Endangered Geodatabase ......")
    arcpy.CopyFeatures_management("lyr", outlocation)

    result = arcpy.GetCount_management(outlocation)
    count = int(result.getOutput(0))
    arcpy.AddMessage("Total Number of Endangered Records: " + str(count))

    cur = arcpy.UpdateCursor(intersectFeatureClass)

    field = "FS_UNIT_ID"

    # populating UnitID field with UnitID_FS field
    for row in cur:
        row.UnitID = row.getValue(field)
        cur.updateRow(row)

    del cur

    # Set local variables
    inFeatures = intersectFeatureClass
    outFeatureClass = intersectFeatureClass + "_noFields"
    dropFields = ["EO_NUMBER", "ACCEPTED_PLANT_CODE", "NRCS_PLANT_CODE","LIFEFORM","DATE_COLLECTED",
                  "DATE_COLLECTED_MOST_RECENT", "CURRENT_MEASUREMENT", "AREA_OCCUPENCY" ,
                  "PLANT_COUNT", "PLANT_COUNT_TYPE" , "ECOLOGICAL_TYPE", "COVER_PCT",
                  "COVER_CLASS_SET_NAME","COVER_CLASS_CODE","SPECIES_LIST_COMPLETENESS","QUALITY_CONTROL",
                  "LOCATIONAL_UNCERTAINTY","SLOPE","ASPECT_AZIMUTH","ASPECT_CARDINAL","ELEVATION_AVERAGE",
                  "EXISTING_VEG_CLASS","POTENTIAL_VEG_CLASS","OWNER_NAME","FS_UNIT_NAME","SOURCE_GEOMETRY_TYPE",
                  "FEATURE_CN","EO_CN","SPATIAL_ID","LAST_UPDATE","PLANT_FOUND","GIS_ACRES","GIS_MILES","EXAMINERS",
                  "BASICOWNERSHIPID", "OWNERCLASSIFICATION", "GIS_ACRES_1", "REGION", "FORESTNAME", "AREA_OCCUPANCY",
                  "SCIENTIFIC_NAME", "ACCEPTED_SCIENTIFIC_NAME", "COMMON_NAME", "ACCEPTED_COMMON_NAME",
                  "ORIG_FID", "FID_USFS_OwnershipLSRS_2017", "REGION_1", "SITE_ID_FS",
                  "FS_UNIT_ID","FORESTNAME_1", "UnitID_FS"]

    # Execute CopyFeatures to make a new copy of the feature class
    #  Use CopyRows if you have a table
    arcpy.CopyFeatures_management(inFeatures, outFeatureClass)

    arcpy.AddMessage("Deleting all unnecessary fields ......")
    # Execute DeleteField
    arcpy.DeleteField_management(outFeatureClass, dropFields)

    arcpy.AddMessage("Repairing Geometry ......")
    arcpy.RepairGeometry_management(outFeatureClass)


    # --------------Copying to Sensitive Geodatabase for interim deliverable step
    arcpy.MakeFeatureLayer_management(outFeatureClass, "lyr")

    arcpy.AddMessage("Selecting records based on Sensitive rank ....")
    arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "GRANK_FIRE = 'Sensitive'")

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

    # --------------Copying to Threatened Geodatabase for interim deliverable step

    arcpy.MakeFeatureLayer_management(outFeatureClass, "lyr")

    arcpy.AddMessage("Selecting records based on Threatened rank ....")
    arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "GRANK_FIRE = 'Threatened'")

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

    # --------------Copying to Endangered Geodatabase for interim deliverable step
    arcpy.MakeFeatureLayer_management(outFeatureClass, "lyr")

    arcpy.AddMessage("Selecting records based on Endangered rank ....")
    arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "GRANK_FIRE = 'Endangered'")

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


except arcpy.ExecuteError:
    arcpy.GetMessages()
except Exception as e:
    arcpy.AddMessage(e)
