# final_merge.py
#
# Usage: Merge_management
# Description: Completes TES processing by merging all the feature classes from each
#              geodatabase into one feature class and a final staging geodatabase
# Created by: Josh Klaus 08/17/2017 jklaus@fs.fed.us
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os
import sys

# in_workspace = sys.argv[1]

in_workspace = "C:\\Users\\jklaus\\Documents\\Python_Testing\\fire_retardant\\"

sr = arcpy.SpatialReference(3310)

arcpy.env.workspace = in_workspace

arcpy.env.overwriteOutput = True

tesvariablelist = ["Endangered", "Threatened", "Sensitive"]

for tes in tesvariablelist:

    newPath = in_workspace + "2017_" + tes

    # Geodatabases for final merge
    merge_gdb = "2017_" + tes + "_Merged_CAALB83.gdb"
    merge_gdb_wkspace = newPath + "\\" + merge_gdb + "\\"

    if arcpy.Exists(merge_gdb_wkspace):
        arcpy.AddMessage(tes + " GDB exists")
    else:
        arcpy.AddMessage("Creating Geodatabase for " + tes + " Data Deliverables containing merged data")
        arcpy.CreateFileGDB_management(newPath, merge_gdb)

final_r05_nodist_gdb = "2017_S_R05_FireRetardantEIS_CAALB83_NoDistribution_FWS.gdb"
final_r05_dist_gdb   = "2017_S_R05_FireRetardantEIS_CAALB83_DistributableDatasets.gdb"

if arcpy.Exists(final_r05_nodist_gdb):
    arcpy.AddMessage("Final FWS GDB not for distribution exists")
else:
    arcpy.AddMessage("Creating Final Geodatabase with non-distributable Data Deliverables containing merged data")
    arcpy.CreateFileGDB_management(in_workspace, final_r05_nodist_gdb)

if arcpy.Exists(final_r05_dist_gdb):
    arcpy.AddMessage("Final GDB with distributable datasets exists")
else:
    arcpy.AddMessage("Creating Final Geodatabase with distrubatable Data Deliverables containing merged data")
    arcpy.CreateFileGDB_management(in_workspace, final_r05_dist_gdb)

final_no_wksp = in_workspace + "\\" + final_r05_nodist_gdb
final_wksp    = in_workspace + "\\" + final_r05_dist_gdb

try:

    for tes in tesvariablelist:
        merge_gdb = "2017_" + tes + "_Merged_CAALB83.gdb"
        newpath = in_workspace + "2017_" + tes
        tes_workspace = newpath + "\\" + "2017_" + tes + "_IdentInter_CAALB83.gdb"
        arcpy.env.workspace = tes_workspace

        if arcpy.Exists(tes_workspace):
            arcpy.AddMessage(tes + " GDB exists")
        else:
            arcpy.AddMessage("Creating Geodatabase for " + tes + " Data Deliverables containing merged data")
            arcpy.CreateFileGDB_management(newpath, merge_gdb)

        fcList = arcpy.ListFeatureClasses()

        inputs = ""

        arcpy.AddMessage("List of features being merged:")
        for fc in fcList:
            inputs += os.path.join(arcpy.env.workspace, fc)
            inputs += ";"
            arcpy.AddMessage("   " + fc)

        merge_fc = newpath + "\\" + merge_gdb + "\\" + "FireRetardantEIS_" + tes + "_Merged"

        arcpy.AddMessage("Merging " + tes + " feature classes")

        arcpy.Merge_management(inputs, merge_fc)

        arcpy.AddMessage("Finished merging " + tes + " feature classes")

        arcpy.AddMessage("Exporting feature class to final non-distributable Geodatabase")

        final_no_fc_old = final_no_wksp + "\\" + "FireRetardantEIS_" + tes + "_Merged"
        final_no_fc = final_no_wksp + "\\" + "FireRetardantEIS_" + tes + "_NoDistribution"

        arcpy.FeatureClassToGeodatabase_conversion(merge_fc, final_no_wksp)

        arcpy.Rename_management(final_no_fc_old, final_no_fc)

        arcpy.AddMessage("Export complete")

        arcpy.AddMessage("Dissolving " + tes + " Features")

        dissolveFeatureClass = final_no_fc + "_dissolved"

        # arcpy.PairwiseDissolve_analysis(intersectFeatureClass, dissolveFeatureClass,["UnitID", "GRANK_FIRE"])

        arcpy.Dissolve_management(final_no_fc, dissolveFeatureClass, ["UnitID", "GRANK_FIRE"], "", "SINGLE_PART")

        arcpy.AddMessage("Repairing Dissolved Geometry ......")
        arcpy.RepairGeometry_management(dissolveFeatureClass)
        arcpy.AddMessage("Dissolve and Repair complete")

        arcpy.FeatureClassToGeodatabase_conversion(dissolveFeatureClass, final_wksp)

        final_fc_old = final_wksp + "\\" + "FireRetardantEIS_" + tes + "_NoDistribution_dissolved"

        final_fc = final_wksp + "\\" + "FireRetardantEIS_" + tes

        arcpy.Rename_management(final_fc_old, final_fc)

    arcpy.AddMessage("Export Complete!!")

except arcpy.ExecuteError:
    arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
    arcpy.AddMessage(e)
