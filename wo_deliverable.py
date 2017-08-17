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

end_workspace = newpath_endangered + "\\" + "2017_Endangered_IdentInter_CAALAB83.gdb"
thr_workspace = newpath_threatened + "\\" + "2017_Threatened_IdentInter_CAALAB83.gdb"
sen_workspace = newpath_sensitive  + "\\" + "2017_Sensitive_IdentInter_CAALAB83.gdb"

final_no_wksp = in_workspace + "\\" + final_r05_nodist_gdb
final_wksp    = in_workspace + "\\" + final_r05_dist_gdb

final_end_fc = final_wksp + "\\" + "FireRetardantEIS_Endangered"
final_thr_fc = final_wksp + "\\" + "FireRetardantEIS_Threatened"
final_sen_fc = final_wksp + "\\" + "FireRetardantEIS_Sensitive"

wo_folder = in_workspace + "WO"

if not os.path.exists(wo_folder):
    arcpy.AddMessage("Creating directory for WO Data Deliverables ....")
    os.makedirs(wo_folder)
    arcpy.AddMessage("Creating Geodatabase for Forest Data Deliverables ....")
    arcpy.CreateFileGDB_management(wo_folder, "S_R05_ANF_FireRetardantEIS.gdb")
    arcpy.CreateFileGDB_management(wo_folder, "S_R05_BDF_FireRetardantEIS.gdb")
    arcpy.CreateFileGDB_management(wo_folder, "S_R05_CNF_FireRetardantEIS.gdb")
    arcpy.CreateFileGDB_management(wo_folder, "S_R05_ENF_FireRetardantEIS.gdb")
    arcpy.CreateFileGDB_management(wo_folder, "S_R05_INF_FireRetardantEIS.gdb")
    arcpy.CreateFileGDB_management(wo_folder, "S_R05_KNF_FireRetardantEIS.gdb")
    arcpy.CreateFileGDB_management(wo_folder, "S_R05_LNF_FireRetardantEIS.gdb")
    arcpy.CreateFileGDB_management(wo_folder, "S_R05_LPF_FireRetardantEIS.gdb")
    arcpy.CreateFileGDB_management(wo_folder, "S_R05_MDF_FireRetardantEIS.gdb")
    arcpy.CreateFileGDB_management(wo_folder, "S_R05_MNF_FireRetardantEIS.gdb")
    arcpy.CreateFileGDB_management(wo_folder, "S_R05_PNF_FireRetardantEIS.gdb")
    arcpy.CreateFileGDB_management(wo_folder, "S_R05_SHF_FireRetardantEIS.gdb")
    arcpy.CreateFileGDB_management(wo_folder, "S_R05_SNF_FireRetardantEIS.gdb")
    arcpy.CreateFileGDB_management(wo_folder, "S_R05_SQF_FireRetardantEIS.gdb")
    arcpy.CreateFileGDB_management(wo_folder, "S_R05_SRF_FireRetardantEIS.gdb")
    arcpy.CreateFileGDB_management(wo_folder, "S_R05_STF_FireRetardantEIS.gdb")
    arcpy.CreateFileGDB_management(wo_folder, "S_R05_TMU_FireRetardantEIS.gdb")
    arcpy.CreateFileGDB_management(wo_folder, "S_R05_TNF_FireRetardantEIS.gdb")

arcpy.MakeFeatureLayer_management(final_end_fc, "lyr" )

arcpy.AddMessage("Selecting records based on Endangered rank ....")

arcpy.SelectLayerByAttribute_management ("lyr", "NEW_SELECTION", "UnitID = '0501'" )

final_wo_space = in_workspace + "\\WO\\" + "S_R05_ANF_FireRetardantEIS.gdb" + "\\" + "FireRetardantEIS_Endangered"

result = arcpy.GetCount_management("lyr")
count = int(result.getOutput(0))
arcpy.AddMessage("Total Number of Records: " + str(count))

if count > 0:
    arcpy.AddMessage("Copying selected records to ANF Geodatabase ......")
    arcpy.CopyFeatures_management("lyr", final_wo_space)


arcpy.MakeFeatureLayer_management(final_thr_fc, "lyr" )

arcpy.AddMessage("Selecting records based on Threatened rank ....")

arcpy.SelectLayerByAttribute_management ("lyr", "NEW_SELECTION", "UnitID = '0501'" )

final_wo_space = in_workspace + "\\WO\\" + "S_R05_ANF_FireRetardantEIS.gdb" + "\\" +final_thr_fc

result = arcpy.GetCount_management("lyr")
count = int(result.getOutput(0))
arcpy.AddMessage("Total Number of Records: " + str(count))

if count > 0:
    arcpy.AddMessage("Copying selected records to ANF Geodatabase ......")
    arcpy.CopyFeatures_management("lyr", final_wo_space)


arcpy.MakeFeatureLayer_management(final_sen_fc, "lyr" )

arcpy.AddMessage("Selecting records based on Sensitive rank ....")

arcpy.SelectLayerByAttribute_management ("lyr", "NEW_SELECTION", "UnitID = '0501'" )

final_wo_space = in_workspace + "\\WO\\" + "S_R05_ANF_FireRetardantEIS.gdb" + "\\" +final_sen_fc

result = arcpy.GetCount_management("lyr")
count = int(result.getOutput(0))
arcpy.AddMessage("Total Number of Records: " + str(count))

if count > 0:
    arcpy.AddMessage("Copying selected records to ANF Geodatabase ......")
    arcpy.CopyFeatures_management("lyr", final_wo_space)

