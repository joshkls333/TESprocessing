# wo_deliverable.py
#
# Description: Creates the final deliverable product for the WO.
#              This includes generating geodatabases for each forest
#              that contains only the status and unitID information
# Created by: Josh Klaus 08/17/2017
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os
import sys

# in_workspace = sys.argv[1]

in_workspace = "C:\\Users\\jklaus\\Documents\\Python_Testing\\fire_retardant\\"

arcpy.env.workspace = in_workspace

arcpy.env.overwriteOutput = True

final_r05_nodist_gdb = "2017_S_R05_FireRetardantEIS_CAALB83_NoDistribution_FWS.gdb"
final_r05_dist_gdb   = "2017_S_R05_FireRetardantEIS_CAALB83_DistributableDatasets.gdb"

final_no_wksp = in_workspace + "\\" + final_r05_nodist_gdb
final_wksp    = in_workspace + "\\" + final_r05_dist_gdb

# final_end_fc = final_wksp + "\\" + "FireRetardantEIS_Endangered"
# final_thr_fc = final_wksp + "\\" + "FireRetardantEIS_Threatened"
# final_sen_fc = final_wksp + "\\" + "FireRetardantEIS_Sensitive"

wo_folder = in_workspace + "WO"

forestGDBList = ["S_R05_ANF_FireRetardantEIS.gdb",
                 "S_R05_BDF_FireRetardantEIS.gdb",
                 "S_R05_CNF_FireRetardantEIS.gdb",
                 "S_R05_ENF_FireRetardantEIS.gdb",
                 "S_R05_INF_FireRetardantEIS.gdb",
                 "S_R05_KNF_FireRetardantEIS.gdb",
                 "S_R05_LNF_FireRetardantEIS.gdb",
                 "S_R05_LPF_FireRetardantEIS.gdb",
                 "S_R05_MDF_FireRetardantEIS.gdb",
                 "S_R05_MNF_FireRetardantEIS.gdb",
                 "S_R05_PNF_FireRetardantEIS.gdb",
                 "S_R05_SHF_FireRetardantEIS.gdb",
                 "S_R05_SNF_FireRetardantEIS.gdb",
                 "S_R05_SQF_FireRetardantEIS.gdb",
                 "S_R05_SRF_FireRetardantEIS.gdb",
                 "S_R05_STF_FireRetardantEIS.gdb",
                 "S_R05_TMU_FireRetardantEIS.gdb",
                 "S_R05_TNF_FireRetardantEIS.gdb" ]

forestGDBDict = {"S_R05_ANF_FireRetardantEIS.gdb": "0501",
                 "S_R05_BDF_FireRetardantEIS.gdb": "0512",
                 "S_R05_CNF_FireRetardantEIS.gdb": "0502",
                 "S_R05_ENF_FireRetardantEIS.gdb": "0503",
                 "S_R05_INF_FireRetardantEIS.gdb": "0504",
                 "S_R05_KNF_FireRetardantEIS.gdb": "0505",
                 "S_R05_LNF_FireRetardantEIS.gdb": "0506",
                 "S_R05_LPF_FireRetardantEIS.gdb": "0507",
                 "S_R05_MDF_FireRetardantEIS.gdb": "0509",
                 "S_R05_MNF_FireRetardantEIS.gdb": "0508",
                 "S_R05_PNF_FireRetardantEIS.gdb": "0511",
                 "S_R05_SHF_FireRetardantEIS.gdb": "0514",
                 "S_R05_SNF_FireRetardantEIS.gdb": "0515",
                 "S_R05_SQF_FireRetardantEIS.gdb": "0513",
                 "S_R05_SRF_FireRetardantEIS.gdb": "0510",
                 "S_R05_STF_FireRetardantEIS.gdb": "0516",
                 "S_R05_TMU_FireRetardantEIS.gdb": "0519",
                 "S_R05_TNF_FireRetardantEIS.gdb": "0517"}

try:
    if not os.path.exists(wo_folder):
        arcpy.AddMessage("Creating directory for WO Data Deliverables ....")
        os.makedirs(wo_folder)
        arcpy.AddMessage("Creating Geodatabase for Forest Data Deliverables ....")
        for forest in forestGDBList:
            arcpy.CreateFileGDB_management(wo_folder, forest)

    tesVariableList = ["Endangered", "Threatened", "Sensitive"]

    for forest in forestGDBList:
        for tes in tesVariableList:
            final_fc = final_wksp + "\\" + "FireRetardantEIS_" + tes
            arcpy.MakeFeatureLayer_management(final_fc, "lyr")
            arcpy.AddMessage("Selecting records based on " + tes + " rank ....")
            unitIDnum = forestGDBDict.get(forest)
            arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "UnitID = '" + unitIDnum + "'")

            final_wo_space = in_workspace + "\\WO\\" + forest + "\\" + "FireRetardantEIS_" + tes

            result = arcpy.GetCount_management("lyr")
            count = int(result.getOutput(0))
            arcpy.AddMessage("Total Number of Records: " + str(count))

            if count > 0:
                arcpy.AddMessage("Copying selected records to " + forest + "  Geodatabase ......")
                arcpy.CopyFeatures_management("lyr", final_wo_space)

except arcpy.ExecuteError:
    arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
    arcpy.AddMessage(e)