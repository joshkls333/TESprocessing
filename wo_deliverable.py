# ---------------------------------------------------------------------------
# wo_deliverable.py
#
# Description: Creates the final deliverable product for the WO.
#              This includes generating geodatabases for each forest
#              that contains only the status and unitID information
#
# Runtime estimates: 3 min 17 sec
#
# Created by: Josh Klaus 08/17/2017 jklaus@fs.fed.us
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os
import sys
import datetime

in_workspace = sys.argv[1]

# in_workspace = "C:\\Users\\jklaus\\Documents\\Python_Testing\\fire_retardant\\"

# using the now variable to assign year every time there is a hardcoded 2017
now = datetime.datetime.today()
curMonth = str(now.month)
curYear = str(now.year)
arcpy.AddMessage("Year is " + curYear)

arcpy.env.workspace = in_workspace

arcpy.env.overwriteOutput = True

# final_end_fc = final_wksp + "\\" + "FireRetardantEIS_Endangered"
# final_thr_fc = final_wksp + "\\" + "FireRetardantEIS_Threatened"
# final_sen_fc = final_wksp + "\\" + "FireRetardantEIS_Sensitive"

wo_folder = in_workspace + "\\" + "WO"
tes_folder = wo_folder + "\\" + "TES_Submitted" + "\\"
fws_folder = wo_folder + "\\" + "FWS" + "\\"

final_r05_nodist_gdb = curYear + "_S_R05_FireRetardantEIS_CAALB83_NoDistribution_FWS.gdb"
final_r05_dist_gdb   = curYear + "_S_R05_FireRetardantEIS_CAALB83_DistributableDatasets.gdb"

final_no_wksp = fws_folder + "\\" + final_r05_nodist_gdb
final_wksp    = fws_folder + "\\" + final_r05_dist_gdb

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
                 "S_R05_SHU_FireRetardantEIS.gdb",
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
                 "S_R05_SHU_FireRetardantEIS.gdb": "0514",
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

    if not os.path.exists(tes_folder):
        arcpy.AddMessage("Creating directory TES_Submitted for WO Data Deliverables of TES forest GDBs....")
        os.makedirs(tes_folder)

    arcpy.AddMessage("Creating Geodatabase for Forest Data Deliverables ....")
    for forest in forestGDBList:
        arcpy.CreateFileGDB_management(tes_folder, forest)

    tesVariableList = ["Endangered", "Threatened", "Sensitive"]

    for forest in forestGDBList:
        arcpy.AddMessage("-----------------------------------------------------------")
        arcpy.AddMessage("Populating " + forest)
        forestFCList = []
        for tes in tesVariableList:
            final_fc = final_wksp + "\\" + "FireRetardantEIS_" + tes
            arcpy.MakeFeatureLayer_management(final_fc, "lyr")
            arcpy.AddMessage("Selecting records based on " + tes + " rank")
            unitIDnum = forestGDBDict.get(forest)
            arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "UnitID = '" + unitIDnum + "'")

            final_wo_space = tes_folder + forest + "\\" + "FireRetardantEIS_" + tes

            result = arcpy.GetCount_management("lyr")
            count = int(result.getOutput(0))
            if count > 0:
                arcpy.AddMessage("Adding feature class for " + tes + " for forest " + forestGDBDict.get(forest))
            else:
                arcpy.AddMessage("There were no records found in " + forestGDBDict.get(forest) + " for " + tes)

            if count > 0:
                arcpy.AddMessage("Copying selected records to " + forest + "  Geodatabase ......")
                arcpy.CopyFeatures_management("lyr", final_wo_space)
                forestFCList.append(final_wo_space)

        mergeFeatureClass = tes_folder + forest + "\\" + "FireRetardantEIS_merge"
        arcpy.AddMessage("Merging Feature Classes")
        arcpy.AddMessage("If there are no files to merge this will error until a workaround is produced!")
        arcpy.Merge_management(forestFCList, mergeFeatureClass)

        arcpy.AddMessage("Dissolving Features")

        dissolveFeatureClass = tes_folder + forest + "\\" + "FireRetardantEIS_Dissolve"

        if sys.version_info[0] < 3:
            arcpy.Dissolve_management(mergeFeatureClass, dissolveFeatureClass, "UnitID")
        else:
            arcpy.PairwiseDissolve_analysis(mergeFeatureClass, dissolveFeatureClass, "UnitID")

except arcpy.ExecuteError:
    arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
    arcpy.AddMessage(e)