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

layerType = "Wildlife_Sites"

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

# outFeatClass = in_workspace + "\\" + layerType + "\\TESP_Test_2017_CAALB83_newproj.gdb\\TESP_2017_Occurrence_found_newE_singlepart_buffer_spart"

outFeatClass = in_workspace + "\\" + layerType + "\\Wildlife_Sites_Test_2017_CAALB83_newproj.gdb\\Wildlife_Sites_2017_Occurrence_found_newE_singlepart_buffer_spart"

# outFeatClass = sys.argv[1]

newpath_threatened = in_workspace + "2017_Threatened"
newpath_endangered = in_workspace + "2017_Endangered"
newpath_sensitive  = in_workspace + "2017_Sensitive"

# Geodatabases for final merge
threatened_gdb = "2017_Threatened_IdentInter_CAALAB83.gdb"
endangered_gdb = "2017_Endangered_IdentInter_CAALAB83.gdb"
sensitive_gdb  = "2017_Sensitive_IdentInter_CAALAB83.gdb"

# Geodatabases for FWS Deliverable
fra_threatened_gdb = "2017_FRA_Threatened_OriginalDataBufferedAndNonBufferedAreas_CAALAB83.gdb"
fra_endangered_gdb = "2017_FRA_Endangered_OriginalDataBufferedAndNonBufferedAreas_CAALAB83.gdb"
fra_sensitive_gdb  = "2017_FRA_Sensitive_OriginalDataBufferedAndNonBufferedAreas_CAALAB83.gdb"

if arcpy.Exists(newpath_sensitive + "\\" + sensitive_gdb):
    arcpy.AddMessage("Sensitive GDB exists")
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

if arcpy.Exists(newpath_threatened + "\\" + threatened_gdb):
        arcpy.AddMessage("Threatened GDB exists")
else:
    arcpy.AddMessage("Creating Geodatabase for Threatened Data Deliverables containing intersection data ....")
    arcpy.CreateFileGDB_management(newpath_threatened, threatened_gdb)
    arcpy.CreateFileGDB_management(newpath_threatened, fra_threatened_gdb)


def copy_to_final_gdb(filename, dissolvedfc):

    tesvariablelist = ["Endangered", "Threatened", "Sensitive"]

    for tes in tesvariablelist:

        arcpy.MakeFeatureLayer_management(dissolvedfc, "tmplyr")

        arcpy.AddMessage("Selecting records based on " + tes + " rank ....")
        arcpy.SelectLayerByAttribute_management("tmplyr", "NEW_SELECTION", "GRANK_FIRE = '" + tes + "'")

        finallocation = in_workspace + "2017_" + tes + "\\2017_" + tes + "_IdentInter_CAALAB83.gdb\\"

        if layerType == "TESP":
            finallocation += "EDW_TESP_2017_" + tes + "_OccurrenceAll_FoundPlants_nobuf"
        elif layerType == "Wildlife_Sites":
            finallocation += "EDW_WildlifeSites_2017_" + tes + "_nobuf"
        elif layerType == "Wildlife_Observations":
            finallocation += "EDW_FishWildlife_Observation_2017_" + tes + "_nobuf"
        elif layerType == "Critical_Habitat_Polygons":
            finallocation += "CHabPolyAllSelectedSpecies_2017_" + tes + "_nobuf"
        elif layerType == "Critical_Habitat_Lines":
            finallocation += "CHabPolyAllSelectedSpecies_2017_" + tes + "_nobuf"
        elif layerType == "CNDDB":
            finallocation += "CNDDB_selects_2017_" + tes + "_nobuf"
        elif layerType == "Condor_Hacking":
            finallocation += "CNH_2017_ident"
        elif layerType == "Condor_Nest":
            finallocation += "CN_2017_ident"
        elif layerType == "Local":
            finallocation += filename

        result = arcpy.GetCount_management("tmplyr")
        count = int(result.getOutput(0))
        arcpy.AddMessage("Total Number of Records: " + str(count))

        if count > 0:
            arcpy.AddMessage("Copying selected records to Final Stage " + tes + " Geodatabase ......")
            arcpy.CopyFeatures_management("tmplyr", finallocation)

    arcpy.AddMessage("Complete copying data to final staging GDB")
    return


def copy_to_interim_gdb(filename):

    tesvariablelist = ["Endangered", "Threatened", "Sensitive"]

    for tes in tesvariablelist:

        arcpy.MakeFeatureLayer_management(intersectFeatureClass, "tmplyr")

        arcpy.AddMessage("Selecting records based on " + tes + " rank ....")
        arcpy.SelectLayerByAttribute_management("tmplyr", "NEW_SELECTION", "GRANK_FIRE = '" + tes + "'")

        outlocation = in_workspace + "2017_" + tes + "\\" + "2017_FRA_" + tes + "_OriginalDataBufferedAndNonBufferedAreas_CAALAB83.gdb" + "\\"

        if layerType == "TESP":
            outlocation += "EDW_TESP_2017_OccurrenceAll_FoundPlants_ident_" + tes
        elif layerType == "Wildlife_Sites":
            outlocation += "EDW_WildlifeSites_2017_ident_" + tes
        elif layerType == "Wildlife_Observations":
            outlocation += "EDW_FishWildlife_Observation_2017_" + tes[:1] + "_ident"
        elif layerType == "Critical_Habitat_Polygons":
            outlocation += "CHabPolyAllSelectedSpecies_2017_nobuf_Ident_" + tes
        elif layerType == "CNDDB":
            outlocation += "CNDDB_2017_All_selectsAndShastaCrayfish_Ident_noBDF_" + tes + "_nobuf"
        elif layerType == "Local":
            outlocation += filename

        result = arcpy.GetCount_management("tmplyr")
        count = int(result.getOutput(0))
        arcpy.AddMessage("Total Number of Records: " + str(count))

        if count > 0:
            arcpy.AddMessage("Copying selected records to FWD Deliverable Stage " + tes + " Geodatabase ......")
            arcpy.CopyFeatures_management("tmplyr", outlocation)

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

            dissolveFC = unitid_dissolve(intersectFeatureClass)

            copy_to_final_gdb(fc, dissolveFC)
    else:

        usfsOwnershipFeatureClass = in_workspace + "\\USFS_Ownership_LSRS\\2017_USFS_Ownership_CAALB83.gdb\\USFS_OwnershipLSRS_2017"

        intersectFeatureClass = outFeatClass + "_intersect"

        arcpy.AddMessage("Intersecting with USFS Ownership feature class .....")
        arcpy.AddMessage("Please be patient while this runs .....")

        arcpy.Intersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)

        # arcpy.PairwiseIntersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)

        arcpy.AddMessage("Completed Intersection")

        copy_to_interim_gdb(layerType)

        dissolveFC = unitid_dissolve(intersectFeatureClass)

        copy_to_final_gdb(layerType, dissolveFC)

    arcpy.AddMessage("Completed Script successfully!!")

except arcpy.ExecuteError:
    arcpy.GetMessages()
except Exception as e:
    arcpy.AddMessage(e)


