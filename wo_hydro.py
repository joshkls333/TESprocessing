# ---------------------------------------------------------------------------
# wo_hydro.py
#
# Description: Creates the final deliverable product for the WO.
#              This includes generating geodatabases for each forest
#
# Runtime Estimates: 2 min 33 sec
#
# Created by: Josh Klaus 08/24/2017 jklaus@fs.fed.us
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os
import sys

# in_workspace = sys.argv[1]

in_workspace = "C:\\Users\\jklaus\\Documents\\Python_Testing\\fire_retardant\\"

arcpy.env.workspace = in_workspace

arcpy.env.overwriteOutput = True

outputWorkSpace = in_workspace + "\\" + "Output" + "\\"

test_hydro_gdb = "Hydro_Test_2017_CAALB83_newproj.gdb"
final_hydro_gdb = "2017_NHDfinal_CAALB83.gdb"
staging_hydro_gdb = "2017_S_R05_FireRetardantEIS_CAALB83_AllHydroDatasets.gdb"

outputHydro = outputWorkSpace + "Hydro2017" + "\\" + test_hydro_gdb

wo_folder = in_workspace + "WO"

hydro_folder = wo_folder + "\\" + "Hydro_Submitted" + "\\"

final_wksp = hydro_folder + "\\" + final_hydro_gdb

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

    if not os.path.exists(hydro_folder):
        arcpy.AddMessage("Creating directory for WO Hydrology Data Deliverables ....")
        os.makedirs(hydro_folder)

        arcpy.AddMessage("Creating Geodatabase for Forest Data Deliverables ....")
        for forest in forestGDBList:
            arcpy.CreateFileGDB_management(hydro_folder, forest)

        arcpy.CreateFileGDB_management(hydro_folder, final_hydro_gdb)

    # May take out after testing is complete
    arcpy.AddMessage("exporting from test gdb to final gdb")
    arcpy.FeatureClassToGeodatabase_conversion(outputHydro +
                                               "\\NHDFlowline_Merge_Buff_intersect_dissolved", final_wksp)
    arcpy.FeatureClassToGeodatabase_conversion(outputHydro +
                                               "\\NHDWaterbody_Area_Merge_Buff_intersect_dissolved", final_wksp)
    arcpy.AddMessage("renaming files to final staging name")
    arcpy.Rename_management(final_wksp + "\\NHDFlowline_Merge_Buff_intersect_dissolved",
                            final_wksp + "\\NHD_Flowline")
    arcpy.Rename_management(final_wksp + "\\NHDWaterbody_Area_Merge_Buff_intersect_dissolved",
                            final_wksp + "\\NHD_Waterbody")

    hydroList = ["NHD_Flowline", "NHD_Waterbody"]

    for forest in forestGDBList:
        for hydro in hydroList:
            final_fc = final_wksp + "\\" + hydro
            arcpy.MakeFeatureLayer_management(final_fc, "lyr")
            arcpy.AddMessage("Selecting records based on " + hydro + " ...")
            unitIDnum = forestGDBDict.get(forest)
            arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", "UnitID = '" + unitIDnum + "'")

            final_wo_space = hydro_folder + forest + "\\" + hydro

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