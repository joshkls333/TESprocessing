# final_merge.py
#
# Usage: Merge_management
# Description: Completes TES processing by merging all the feature classes from each
#              geodatabase into one feature class and a final staging geodatabase
# Created by: Josh Klaus 08/17/2017
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

newpath_threatened = in_workspace + "2017_Threatened"
newpath_endangered = in_workspace + "2017_Endangered"
newpath_sensitive  = in_workspace + "2017_Sensitive"

merge_threatened_gdb = "2017_Threatened_Merged_CAALAB83.gdb"
merge_endangered_gdb = "2017_Endangered_Merged_CAALAB83.gdb"
merge_sensitive_gdb  = "2017_Sensitive_Merged_CAALAB83.gdb"

final_r05_nodist_gdb = "2017_S_R05_FireRetardantEIS_CAALB83_NoDistribution_FWS.gdb"
final_r05_dist_gdb   = "2017_S_R05_FireRetardantEIS_CAALB83_DistributableDatasets.gdb"

merge_thr_gdb_wkspace = newpath_threatened + "\\" + merge_threatened_gdb + "\\"
merge_end_gdb_wkspace = newpath_endangered + "\\" + merge_endangered_gdb + "\\"
merge_sen_gdb_wkspace = newpath_sensitive + "\\" + merge_sensitive_gdb + "\\"

if arcpy.Exists(merge_sen_gdb_wkspace):
    arcpy.AddMessage("Sensitive GDB exists")
else:
    arcpy.AddMessage("Creating Geodatabase for Sensitive Data Deliverables containing merged data")
    arcpy.CreateFileGDB_management(newpath_sensitive, merge_sensitive_gdb)

if arcpy.Exists(merge_end_gdb_wkspace):
    arcpy.AddMessage("Endangered GDB exists")
else:
    arcpy.AddMessage("Creating Geodatabase for Endangered Data Deliverables containing merged data")
    arcpy.CreateFileGDB_management(newpath_endangered, merge_endangered_gdb)

if arcpy.Exists(merge_thr_gdb_wkspace):
    arcpy.AddMessage("Threatened GDB exists")
else:
    arcpy.AddMessage("Creating Geodatabase for Threatened Data Deliverables containing merged data")
    arcpy.CreateFileGDB_management(newpath_threatened, merge_threatened_gdb)

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

end_workspace = newpath_endangered + "\\" + "2017_Endangered_IdentInter_CAALAB83.gdb"
thr_workspace = newpath_threatened + "\\" + "2017_Threatened_IdentInter_CAALAB83.gdb"
sen_workspace = newpath_sensitive  + "\\" + "2017_Sensitive_IdentInter_CAALAB83.gdb"

final_no_wksp = in_workspace + "\\" + final_r05_nodist_gdb
final_wksp    = in_workspace + "\\" + final_r05_dist_gdb

arcpy.env.workspace = end_workspace

fcList = arcpy.ListFeatureClasses()

end_inputs = ""

arcpy.AddMessage("List of features being merged:")
for fc in fcList:
    end_inputs += os.path.join(arcpy.env.workspace, fc)
    end_inputs += ";"
    arcpy.AddMessage("   " + fc)

end_inputs = end_inputs.replace("\\", "\\\\")

merge_end_fc = merge_end_gdb_wkspace + "\\" + "FireRetardantEIS_Endangered_Merged"

arcpy.AddMessage("Merging Endangered feature classes")

arcpy.Merge_management(end_inputs, merge_end_fc)

arcpy.AddMessage("Finished merging endangered feature classes")

arcpy.env.workspace = thr_workspace

fcList = arcpy.ListFeatureClasses()

thr_inputs = ""

arcpy.AddMessage("List of features being merged:")
for fc in fcList:
    thr_inputs += os.path.join(arcpy.env.workspace, fc)
    thr_inputs += ";"
    arcpy.AddMessage("   " + fc)

thr_inputs = thr_inputs.replace("\\", "\\\\")

merge_thr_fc = merge_thr_gdb_wkspace + "\\" + "FireRetardantEIS_Threatened_Merged"

arcpy.AddMessage("Merging Threatened feature classes")

arcpy.Merge_management(thr_inputs, merge_thr_fc)

arcpy.AddMessage("Finished merging threatened feature classes")

arcpy.env.workspace = sen_workspace

fcList = arcpy.ListFeatureClasses()

sen_inputs = ""

arcpy.AddMessage("List of features being merged:")
for fc in fcList:
    sen_inputs += os.path.join(arcpy.env.workspace, fc)
    sen_inputs += ";"
    arcpy.AddMessage("   " + fc)

sen_inputs = sen_inputs.replace("\\", "\\\\")

merge_sen_fc = merge_sen_gdb_wkspace + "\\" + "FireRetardantEIS_Sensitive_Merged"

arcpy.AddMessage("Merging Sensitive feature classes")

arcpy.Merge_management(sen_inputs, merge_sen_fc)

arcpy.AddMessage("Finished merging sensitive feature classes")

arcpy.AddMessage("Exporting feature class to final non-distributable Geodatabase")

final_no_end_fc_old = final_no_wksp + "\\" + "FireRetardantEIS_Endangered_Merged"
final_no_thr_fc_old = final_no_wksp + "\\" + "FireRetardantEIS_Threatened_Merged"
final_no_sen_fc_old = final_no_wksp + "\\" + "FireRetardantEIS_Sensitive_Merged"

final_no_end_fc = final_no_wksp + "\\" + "FireRetardantEIS_Endangered_NoDistribution"
final_no_thr_fc = final_no_wksp + "\\" + "FireRetardantEIS_Threatened_NoDistribution"
final_no_sen_fc = final_no_wksp + "\\" + "FireRetardantEIS_Sensitive_NoDistribution"

arcpy.FeatureClassToGeodatabase_conversion(merge_end_fc, final_no_wksp)
arcpy.FeatureClassToGeodatabase_conversion(merge_thr_fc, final_no_wksp)
arcpy.FeatureClassToGeodatabase_conversion(merge_sen_fc, final_no_wksp)

arcpy.Rename_management(final_no_end_fc_old,final_no_end_fc)
arcpy.Rename_management(final_no_thr_fc_old,final_no_thr_fc)
arcpy.Rename_management(final_no_sen_fc_old,final_no_sen_fc)

arcpy.AddMessage("Export complete")

arcpy.AddMessage("Dissolving Endangered Features")

dissolveEndFeatureClass = final_no_end_fc + "_dissolved"

# arcpy.PairwiseDissolve_analysis(intersectFeatureClass, dissolveFeatureClass,["UnitID", "GRANK_FIRE"])

arcpy.Dissolve_management(final_no_end_fc, dissolveEndFeatureClass,["UnitID", "GRANK_FIRE"], "", "SINGLE_PART")

arcpy.AddMessage("Repairing Dissolved Geometry ......")
arcpy.RepairGeometry_management(dissolveEndFeatureClass)
arcpy.AddMessage("Dissolve and Repair complete")

arcpy.AddMessage("Dissolving Threatened Features")

dissolveThrFeatureClass = final_no_thr_fc + "_dissolved"

# arcpy.PairwiseDissolve_analysis(intersectFeatureClass, dissolveFeatureClass,["UnitID", "GRANK_FIRE"])

arcpy.Dissolve_management(final_no_thr_fc, dissolveThrFeatureClass,["UnitID", "GRANK_FIRE"], "", "SINGLE_PART")

arcpy.AddMessage("Repairing Dissolved Geometry ......")
arcpy.RepairGeometry_management(dissolveThrFeatureClass)
arcpy.AddMessage("Dissolve and Repair complete")

arcpy.AddMessage("Dissolving Sensitive Features")

dissolveSenFeatureClass = final_no_sen_fc + "_dissolved"

# arcpy.PairwiseDissolve_analysis(intersectFeatureClass, dissolveFeatureClass,["UnitID", "GRANK_FIRE"])

arcpy.Dissolve_management(final_no_sen_fc, dissolveSenFeatureClass,["UnitID", "GRANK_FIRE"], "", "SINGLE_PART")

arcpy.AddMessage("Repairing Dissolved Geometry ......")
arcpy.RepairGeometry_management(dissolveSenFeatureClass)
arcpy.AddMessage("Dissolve and Repair complete")

arcpy.AddMessage("Exporting dissolved feature classes to final distributable Geodatabase")

arcpy.FeatureClassToGeodatabase_conversion(dissolveEndFeatureClass, final_wksp)
arcpy.FeatureClassToGeodatabase_conversion(dissolveThrFeatureClass, final_wksp)
arcpy.FeatureClassToGeodatabase_conversion(dissolveSenFeatureClass, final_wksp)

final_end_fc_old = final_wksp + "\\" + "FireRetardantEIS_Endangered_NoDistribution_dissolved"
final_thr_fc_old = final_wksp + "\\" + "FireRetardantEIS_Threatened_NoDistribution_dissolved"
final_sen_fc_old = final_wksp + "\\" + "FireRetardantEIS_Sensitive_NoDistribution_dissolved"

final_end_fc = final_wksp + "\\" + "FireRetardantEIS_Endangered"
final_thr_fc = final_wksp + "\\" + "FireRetardantEIS_Threatened"
final_sen_fc = final_wksp + "\\" + "FireRetardantEIS_Sensitive"

arcpy.Rename_management(final_end_fc_old,final_end_fc)
arcpy.Rename_management(final_thr_fc_old,final_thr_fc)
arcpy.Rename_management(final_sen_fc_old,final_sen_fc)

arcpy.AddMessage("Export Complete!!")



