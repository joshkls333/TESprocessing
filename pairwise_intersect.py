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
local_gdb = in_workspace + "\\Local_Data\\2017_Local_CAALB83.gdb\\"
local_data = local_gdb + "\\Explode"

# layerType = "Condor_Hacking"

# layerType = "NOAA_ESU"

layerType = sys.argv[2]

# nameOfFile = sys.argv[3]

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


# intable = r"C:\Users\jklaus\Documents\Python_Testing\fire_retardant\2017_EDW_CAALB83.gdb\EDW_TESP_2017_OccurrenceAll_FoundPlants_newH_"

# outFeatClass = in_workspace + "\\" + layerType + "\\Critical_Habitat_Polygons_Test_2017_CAALB83_newproj.gdb\Critical_Habitat_Polygons_2017_Occurrence_found_newE_singlepart"

# outFeatClass = in_workspace + "\\" + layerType + "\\TESP_Test_2017_CAALB83_newproj.gdb\\TESP_2017_Occurrence_found_newE_singlepart_buffer_spart"

# outFeatClass = in_workspace + "\\" + layerType + "\\Wildlife_Sites_Test_2017_CAALB83_newproj.gdb\\Wildlife_Sites_2017_Occurrence_found_newE_singlepart_buffer_spart"

# outFeatClass = in_workspace + "\\CondorData_noFOIAnoRelease\\2017_Condor_CAALB83.gdb\\CondorHacking_2015"


outFeatClass = sys.argv[1]

nameOfFile = outFeatClass

nameOfFile = nameOfFile.replace('C:\\Users\\jklaus\\Documents\\Python_Testing\\fire_retardant\\NOAA_ESU\\2017_NOAA_ESU_CAALB83.gdb\\','')
arcpy.AddMessage(nameOfFile)

tesvariablelist = ["Endangered", "Threatened", "Sensitive"]

for tes in tesvariablelist:

    newPath = in_workspace + "2017_" + tes

# newpath_threatened = in_workspace + "2017_Threatened"
# newpath_endangered = in_workspace + "2017_Endangered"
# newpath_sensitive  = in_workspace + "2017_Sensitive"

# Geodatabases for final merge
    identInterGdb = "2017_" + tes + "_IdentInter_CAALB83.gdb"

# threatened_gdb = "2017_Threatened_IdentInter_CAALB83.gdb"
# endangered_gdb = "2017_Endangered_IdentInter_CAALB83.gdb"
# sensitive_gdb  = "2017_Sensitive_IdentInter_CAALB83.gdb"

# Geodatabases for FWS Deliverable
    fraDeliverableGdb = "2017_FRA_" + tes + "_OriginalDataBufferedAndNonBufferedAreas_CAALB83.gdb"

# fra_threatened_gdb = "2017_FRA_Threatened_OriginalDataBufferedAndNonBufferedAreas_CAALB83.gdb"
# fra_endangered_gdb = "2017_FRA_Endangered_OriginalDataBufferedAndNonBufferedAreas_CAALB83.gdb"
# fra_sensitive_gdb  = "2017_FRA_Sensitive_OriginalDataBufferedAndNonBufferedAreas_CAALB83.gdb"

    if arcpy.Exists( newPath + "\\" + identInterGdb):
        arcpy.AddMessage(tes + " GDB exists")
    else:
        arcpy.AddMessage("Creating Geodatabase for " + tes + " Data Deliverables containing intersection data ....")
        arcpy.CreateFileGDB_management(newPath, identInterGdb)
        arcpy.CreateFileGDB_management(newPath, fraDeliverableGdb)

# if arcpy.Exists(newpath_sensitive + "\\" + sensitive_gdb):
#     arcpy.AddMessage("Sensitive GDB exists")
# else:
#     arcpy.AddMessage("Creating Geodatabase for Sensitive Data Deliverables containing intersection data ....")
#     arcpy.CreateFileGDB_management(newpath_sensitive, sensitive_gdb)
#     arcpy.CreateFileGDB_management(newpath_sensitive, fra_sensitive_gdb)
#
# if arcpy.Exists(newpath_endangered + "\\" + endangered_gdb):
#     arcpy.AddMessage("Endangered GDB exists")
# else:
#     arcpy.AddMessage("Creating Geodatabase for Endangered Data Deliverables containing intersection data ....")
#     arcpy.CreateFileGDB_management(newpath_endangered, endangered_gdb)
#     arcpy.CreateFileGDB_management(newpath_endangered, fra_endangered_gdb)
#
# if arcpy.Exists(newpath_threatened + "\\" + threatened_gdb):
#         arcpy.AddMessage("Threatened GDB exists")
# else:
#     arcpy.AddMessage("Creating Geodatabase for Threatened Data Deliverables containing intersection data ....")
#     arcpy.CreateFileGDB_management(newpath_threatened, threatened_gdb)
#     arcpy.CreateFileGDB_management(newpath_threatened, fra_threatened_gdb)


def copy_to_final_gdb(filename, dissolvedfc):

    tesvariablelist = ["Endangered", "Threatened", "Sensitive"]

    for tes in tesvariablelist:
        arcpy.AddMessage(" --------------------------------------------------------------- ")

        arcpy.MakeFeatureLayer_management(dissolvedfc, "tmplyr")

        arcpy.AddMessage("Selecting records based on " + tes + " rank ....")
        arcpy.SelectLayerByAttribute_management("tmplyr", "NEW_SELECTION", "GRANK_FIRE = '" + tes + "'")

        finallocation = in_workspace + "2017_" + tes + "\\2017_" + tes + "_IdentInter_CAALB83.gdb\\"

        if layerType == "TESP":
            outputname = "EDW_TESP_2017_" + tes + "_OccurrenceAll_FoundPlants_nobuf"
        elif layerType == "Wildlife_Sites":
            outputname = "EDW_WildlifeSites_2017_" + tes + "_nobuf"
        elif layerType == "Wildlife_Observations":
            outputname = "EDW_FishWildlife_Observation_2017_" + tes + "_nobuf"
        elif layerType == "Critical_Habitat_Polygons":
            outputname = "CHabPolyAllSelectedSpecies_2017_" + tes + "_nobuf"
        elif layerType == "Critical_Habitat_Lines":
            outputname = "CHabLineAllSelectedSpecies_2017_" + tes + "_nobuf"
        elif layerType == "CNDDB":
            outputname = "CNDDB_selects_2017_" + tes + "_nobuf"
        elif layerType == "Condor_Hacking":
            outputname = "CNH_2017_ident"
        elif layerType == "Condor_Nest":
            outputname = "CN_2017_ident"
        elif layerType == "Local" or layerType == "NOAA_ESU":
            outputname = filename

        finallocation += outputname

        result = arcpy.GetCount_management("tmplyr")
        count = int(result.getOutput(0))
        arcpy.AddMessage("Total Number of Records: " + str(count))

        if count > 0:
            arcpy.AddMessage("Copying " + layerType + " records to Final Stage " +
                             tes + " Geodatabase as " + outputname)
            arcpy.CopyFeatures_management("tmplyr", finallocation)
        else:
            arcpy.AddMessage("No records found for rank " + tes)

    arcpy.AddMessage("Complete copying data to final staging GDB")
    arcpy.AddMessage(" ____________________________________________________________________")
    return


def copy_to_interim_gdb(filename):

    tesvariablelist = ["Endangered", "Threatened", "Sensitive"]

    for tes in tesvariablelist:
        arcpy.AddMessage(" --------------------------------------------------------------- ")

        arcpy.MakeFeatureLayer_management(intersectFeatureClass, "tmplyr")

        arcpy.AddMessage("Selecting records based on " + tes + " rank ....")
        arcpy.SelectLayerByAttribute_management("tmplyr", "NEW_SELECTION", "GRANK_FIRE = '" + tes + "'")

        outlocation = in_workspace + "2017_" + tes + "\\" + "2017_FRA_" + \
                      tes + "_OriginalDataBufferedAndNonBufferedAreas_CAALB83.gdb" + "\\"

        if layerType == "TESP":
            interimoutput = "EDW_TESP_2017_OccurrenceAll_FoundPlants_ident_" + tes
        elif layerType == "Wildlife_Sites":
            interimoutput = "EDW_WildlifeSites_2017_ident_" + tes
        elif layerType == "Wildlife_Observations":
            interimoutput = "EDW_FishWildlife_Observation_2017_" + tes[:1] + "_ident"
        elif layerType == "Critical_Habitat_Polygons":
            interimoutput = "CHabPolyAllSelectedSpecies_2017_nobuf_Ident_" + tes
        elif layerType == "Critical_Habitat_Lines":
            interimoutput = "CHabLineAllSelectedSpecies_2017_nobuf_Ident_" + tes
        elif layerType == "CNDDB":
            interimoutput = "CNDDB_2017_All_selectsAndShastaCrayfish_Ident_noBDF_" + tes
        elif layerType == "Local" or layerType == "NOAA_ESU":
            interimoutput = filename

        outlocation += interimoutput

        result = arcpy.GetCount_management("tmplyr")
        count = int(result.getOutput(0))
        arcpy.AddMessage("Total Number of Records: " + str(count))

        if count > 0:
            arcpy.AddMessage("Copying " + layerType + " records to FWS Deliverable Stage " +
                             tes + " Geodatabase as " + interimoutput)
            arcpy.CopyFeatures_management("tmplyr", outlocation)
        else:
            arcpy.AddMessage("No records found for rank " + tes)

    arcpy.AddMessage("Complete copying data to interim deliverable GDB for Fish and Wildlife")
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

    if layerType == "CNDDB":
        arcpy.AddMessage("Total records deleted because they were Plants from San Bernardino : " + str(plant0512num))

    if layerType == "CNDDB":
        with arcpy.da.UpdateCursor(intersectFeatureClass, ["Type", "UnitID"]) as cursor:
            for row in cursor:
                if row[0] == "PLANT" and row[1] == "0512":
                    cursor.deleteRow()
                    arcpy.AddMessage("Deleted row")

    arcpy.AddMessage("Repairing Geometry ......")
    arcpy.RepairGeometry_management(filename)

    arcpy.AddMessage("Dissolving Features")

    dissolveFeatureClass = filename + "_dissolved"

    arcpy.PairwiseDissolve_analysis(intersectFeatureClass, dissolveFeatureClass,
                              ["UnitID", "GRANK_FIRE", "SNAME_FIRE", "CNAME_FIRE", "SOURCEFIRE",
                               "BUFFT_FIRE", "BUFFM_FIRE", "CMNT_FIRE", "INST_FIRE"])

    # arcpy.Dissolve_management(filename, dissolveFeatureClass,
    #                                 ["UnitID", "GRANK_FIRE", "SNAME_FIRE", "CNAME_FIRE", "SOURCEFIRE",
    #                                  "BUFFT_FIRE", "BUFFM_FIRE", "CMNT_FIRE", "INST_FIRE"],"","SINGLE_PART")

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

    if layerType == "Local":
    # if layerType == "Local" or layerType == "NOAA_ESU":
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

            arcpy.Intersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)

            # arcpy.PairwiseIntersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)

            arcpy.AddMessage("Completed Intersection")

            copy_to_interim_gdb(fc)

            dissolveFC = unitid_dissolve(intersectFeatureClass)

            copy_to_final_gdb(fc, dissolveFC)
    else:

        usfsOwnershipFeatureClass = in_workspace + \
                                    "\\USFS_Ownership_LSRS\\2017_USFS_Ownership_CAALB83.gdb\\USFS_OwnershipLSRS_2017"

        intersectFeatureClass = outFeatClass + "_intersect"

        arcpy.AddMessage("Intersecting with USFS Ownership feature class .....")
        arcpy.AddMessage("Please be patient while this runs .....")

        # arcpy.Intersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)

        arcpy.PairwiseIntersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)

        arcpy.AddMessage("Completed Intersection")

        if layerType != "Condor_Nest" and layerType != "Condor_Hacking":
            if layerType == "NOAA_ESU":
                copy_to_interim_gdb(nameOfFile)
            else:
                copy_to_interim_gdb(outFeatClass)

        dissolveFC = unitid_dissolve(intersectFeatureClass)

        if layerType == "NOAA_ESU":
            copy_to_final_gdb(nameOfFile, dissolveFC)
        else:
            copy_to_final_gdb(layerType, dissolveFC)

    arcpy.AddMessage("Completed Script successfully!!")

except arcpy.ExecuteError:
    arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
    arcpy.AddMessage(e)


