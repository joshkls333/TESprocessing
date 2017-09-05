# ---------------------------------------------------------------------------
# pairwise_intersect.py
#
# Usage: PairwiseIntersect_analysis
# Description: Performs an Intersect_analysis with pairwise processing that only
#              runs in ArcGIS Pro. After the intersection data is exported to FWS GDB.
#              UnitID field is populated based on intersection and a Dissolve is performed
#              to dissolve data and remove extraneous fields. Data is exported to Final
#              GDB.
#              Note: User selects final file from preprocessing for all datasets except Local
#                     and NOAA. Those two datasets will generate a list of feature classes and
#                     loop through them running intersection and export processes.
#
# Runtime Estimates: NOAA       : 29 min 52 sec
#                    Local      : 16 min 20 sec
#                    TESP       :  1 min  2 sec
#                    Wild Sites :        33 sec
#                    Wild Obs E :  2 min 16 sec
#                    Wild Obs T :  1 min  4 sec
#                    Wild obs S :        22 sec
#                    CHab Poly  :        26 sec
#                    Chab Line  :        11 sec
#                    CNDDB      :        48 sec
#                    Cond Nest  :        18 sec
#                    Cond Hack  :        16 sec
#
# Created by: Josh Klaus 08/01/2017 jklaus@fs.fed.us
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import sys
import csv

in_workspace = sys.argv[1]

in_workspace = "C:\\Users\\jklaus\\Documents\\Python_Testing\\fire_retardant\\"
local_gdb = in_workspace + "\\Local_Data\\2017_Local_CAALB83.gdb\\"
local_data = local_gdb + "\\Explode"

# layerType = "Condor_Hacking"

# layerType = "Local"

# layerType = "NOAA_ESU"

# layerType = "CNDDB"

layerType = sys.argv[3]

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

# The following is used for testing locally. DELETE when done testing.
# outFeatClass = in_workspace + "\\" + layerType + "\\Critical_Habitat_Polygons_Test_2017_CAALB83_newproj.gdb\Critical_Habitat_Polygons_2017_Occurrence_found_newE_singlepart"

# outFeatClass = in_workspace + "\\" + "Output" + "\\" + layerType + "\\TESP_Test_2017_CAALB83_newproj.gdb\\TESP_2017_original_buffered_single"

# outFeatClass = in_workspace + "\\" + layerType + "\\Wildlife_Sites_Test_2017_CAALB83_newproj.gdb\\Wildlife_Sites_2017_Occurrence_found_newE_singlepart_buffer_spart"

# outFeatClass = in_workspace + "\\CondorData_noFOIAnoRelease\\2017_Condor_CAALB83.gdb\\CondorHacking_2015"

# outFeatClass = in_workspace + "\\Output\\CNDDB\\CNDDB_Test_2017_CAALB83_newproj.gdb\\CNDDB_2017_original_merge"

outFeatClass = sys.argv[2]

nameOfFile = outFeatClass

nameOfFile = nameOfFile.replace('C:\\Users\\jklaus\\Documents\\Python_Testing\\fire_retardant\\NOAA_ESU\\2017_NOAA_ESU_CAALB83.gdb\\','')
arcpy.AddMessage(nameOfFile)

tesvariablelist = ["Endangered", "Threatened", "Sensitive"]

for tes in tesvariablelist:

    newPath = in_workspace + "2017_" + tes

    # Geodatabases for final merge
    identInterGdb = "2017_" + tes + "_IdentInter_CAALB83.gdb"

    # Geodatabases for FWS Deliverable
    fraDeliverableGdb = "2017_FRA_" + tes + "_OriginalDataBufferedAndNonBufferedAreas_CAALB83.gdb"

    if arcpy.Exists( newPath + "\\" + identInterGdb):
        arcpy.AddMessage(tes + " GDB exists")
    else:
        arcpy.AddMessage("Creating Geodatabase for " + tes + " Data Deliverables containing intersection data ....")
        arcpy.CreateFileGDB_management(newPath, identInterGdb)
        arcpy.CreateFileGDB_management(newPath, fraDeliverableGdb)


def get_filename(tes_rank, orig_filename):

    filename = ""
    if layerType == "TESP":
        filename = "EDW_TESP_2017_OccurrenceAll_FoundPlants_ident_" + tes_rank
    elif layerType == "Wildlife_Sites":
        filename = "EDW_WildlifeSites_2017_ident_" + tes_rank
    elif layerType == "Wildlife_Observations":
        filename = "EDW_FishWildlife_Observation_2017_" + tes_rank[:1] + "_ident"
    elif layerType == "Critical_Habitat_Polygons":
        filename = "CHabPolyAllSelectedSpecies_2017_nobuf_Ident_" + tes_rank
    elif layerType == "Critical_Habitat_Lines":
        filename = "CHabLineAllSelectedSpecies_2017_nobuf_Ident_" + tes_rank
    elif layerType == "CNDDB":
        filename = "CNDDB_2017_All_selectsAndShastaCrayfish_Ident_noBDF_" + tes_rank
    elif layerType == "Condor_Hacking":
        filename = "CNH_2017_ident"
    elif layerType == "Condor_Nest":
        filename = "CN_2017_ident"
    elif layerType == "Local" or layerType == "NOAA_ESU":
        filename = fc

    return filename


def copy_to_gdb(stage, filename):

    for tes_rank in tesvariablelist:
        arcpy.AddMessage(" --------------------------------------------------------------- ")

        arcpy.MakeFeatureLayer_management(filename, "tmplyr")

        arcpy.AddMessage("Selecting records based on " + tes_rank + " rank ....")
        arcpy.SelectLayerByAttribute_management("tmplyr", "NEW_SELECTION", "GRANK_FIRE = '" + tes_rank + "'")

        if stage == "Interim":
            outlocation = in_workspace + "2017_" + tes_rank + "\\" + "2017_FRA_" + \
                          tes_rank + "_OriginalDataBufferedAndNonBufferedAreas_CAALB83.gdb" + "\\"
        else:
            outlocation = in_workspace + "2017_" + tes_rank + "\\2017_" + tes_rank + "_IdentInter_CAALB83.gdb\\"

        outputfilename = get_filename(tes_rank, filename)

        outlocation += outputfilename

        result = arcpy.GetCount_management("tmplyr")
        count = int(result.getOutput(0))
        arcpy.AddMessage("Total Number of Records: " + str(count))

        if count > 0:
            if stage == "Interim":
                arcpy.AddMessage("Copying " + layerType + " records to FWS Deliverable Stage " +
                             tes_rank + " Geodatabase as " + outputfilename)
            else:
                arcpy.AddMessage("Copying " + layerType + " records to Final Stage " +
                             tes_rank + " Geodatabase as " + outputfilename)
            arcpy.CopyFeatures_management("tmplyr", outlocation)
        else:
            arcpy.AddMessage("No records found for rank " + tes_rank)

    arcpy.AddMessage("Complete copying data to " + stage + " staging GDB")
    arcpy.AddMessage(" ____________________________________________________________________")
    return

def unitid_dissolve(filename):
    arcpy.AddMessage(" ____________________________________________________________________")

    arcpy.AddMessage("Updating UnitID field from intersection")

    cur = arcpy.UpdateCursor(filename)

    field = "UnitID_FS"
    fieldrank = "GRANK_FIRE"
    fieldforest = "FORESTNAME"
    fieldother = "Type"
    fieldspecies = "SNAME_FIRE"
    plant0512num = 0
    ranaboyliinum = 0

    csvfile = in_workspace + "\\csv_tables\CNDDB_SummaryTable.csv"

    arcpy.AddMessage("csv File: " + csvfile)
    arcpy.AddMessage("NOTE: Code will operate differently for csv in Pro vs 10.x!!!!!")
    arcpy.AddMessage("Version of Python: " + sys.version)

    if sys.version_info[0] < 3:
        # uncomment when using arcgis 10.3
        with open(csvfile, 'rb') as f:
            reader = csv.reader(f)
            selectionList = list(reader)
    else:
        # use when using arcgis pro
        with open(csvfile) as f:
            reader = csv.reader(f)
            selectionList = list(reader)

    # populating UnitID field with UnitID_FS field
    for row in cur:
        speciesname = row.getValue(fieldspecies)
        forestname = row.getValue(fieldforest)
        row.UnitID = "0" + str(row.getValue(field))
        cur.updateRow(row)
        if layerType == "Wildlife_Observations":
            if speciesname == "Oncorhynchus kisutch" \
                    and str(row.getValue(field)) == "516":
                cur.deleteRow(row)
                arcpy.AddMessage(
                    "Deleting row for Oncorhynchus kisutch because forest not protected, found in " + forestname)
        elif layerType == "Critical_Habitat_Polygons":
            if speciesname == "Rana muscosa" \
                    and str(row.getValue(field)) != "501" \
                    and str(row.getValue(field)) != "512" \
                    and str(row.getValue(field)) != "502" \
                    and str(row.getValue(field)) != "507":
                cur.deleteRow(row)
                arcpy.AddMessage(
                    "Deleting row for Rana muscosa because not Southern forest species, found in " + forestname)
        # Used for filtering out records in CNDDB
        elif layerType == "CNDDB":
            # Used for deleting all the plant records in San Bernardino for CNDDB
            if str(row.getValue(field)) == "512" \
                    and row.getValue(fieldrank) != "Sensitive" \
                    and row.getValue(fieldother) == "PLANT":
                cur.deleteRow(row)
                plant0512num += 1
                arcpy.AddMessage("deleted a row for 0512 Plant: " + speciesname)
            # Used for deleting all the Rana boylii not in the following three forests
            elif str(row.getValue(field)) != "507" \
                    and str(row.getValue(field)) != "513" \
                    and str(row.getValue(field)) != "515" \
                    and speciesname == "Rana boylii":
                cur.deleteRow(row)
                ranaboyliinum += 1
                arcpy.AddMessage("deleted a row for Rana boylii in forest: " + forestname)
            # elif (str(row.getValue(field)) == "508" \
            #         or str(row.getValue(field)) == "514" \
            #         or str(row.getValue(field)) == "510" \
            #         or str(row.getValue(field)) == "505") \
            #         and speciesname == "Rana muscosa":
            #     cur.deleteRow(row)
            #     arcpy.AddMessage("deleted a row for Rana muscosa in forest: " + forestname)
            else:
                # Used for deleting all the species selected not in a particular forest
                for item in selectionList:
                    if item[0].startswith(speciesname) and speciesname != "Rana boylii" and speciesname != "Rana muscosa":
                        if item[3] == "":
                            break
                        elif item[3] != forestname.upper():
                            cur.deleteRow(row)
                            arcpy.AddMessage("deleted row for " + speciesname +
                                             " because found in " + forestname)

    del cur

    # running export to gdb just for CNDDB dataset others were ran prior to this function
    if layerType == "CNDDB":
        arcpy.AddMessage("Total records deleted because they were Plants from San Bernardino : " + str(plant0512num))
        arcpy.AddMessage("Total records deleted because they were Rana boylii not in target forests : " + str(ranaboyliinum))
        copy_to_gdb("Interim", filename)

    arcpy.AddMessage("Repairing Geometry ......")
    arcpy.RepairGeometry_management(filename)

    arcpy.AddMessage("Dissolving Features")

    dissolveFeatureClass = filename + "_dissolved"

    if sys.version_info[0] < 3:
        arcpy.Dissolve_management(filename, dissolveFeatureClass,
                                        ["UnitID", "GRANK_FIRE", "SNAME_FIRE", "CNAME_FIRE", "SOURCEFIRE",
                                         "BUFFT_FIRE", "BUFFM_FIRE", "CMNT_FIRE", "INST_FIRE"], "", "SINGLE_PART")
    else:
        arcpy.PairwiseDissolve_analysis(intersectFeatureClass, dissolveFeatureClass,
                              ["UnitID", "GRANK_FIRE", "SNAME_FIRE", "CNAME_FIRE", "SOURCEFIRE",
                               "BUFFT_FIRE", "BUFFM_FIRE", "CMNT_FIRE", "INST_FIRE"])


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

    # if layerType == "Local":
    if layerType == "Local" or layerType == "NOAA_ESU":
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

            if layerType == "Local":
                arcpy.Intersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)
            else:
                if sys.version_info[0] < 3:
                    arcpy.AddMessage("Python version of ArcGIS 10.x requires Intersect_analysis.")
                    arcpy.AddMessage("Switch to ArcGIS Pro to use Pairwise Intersection and reduce runtime.")
                    arcpy.Intersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)
                else:
                    arcpy.PairwiseIntersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)

            arcpy.AddMessage("Completed Intersection")

            copy_to_gdb("Interim", intersectFeatureClass)

            dissolveFC = unitid_dissolve(intersectFeatureClass)

            copy_to_gdb("Final", dissolveFC)
    else:

        usfsOwnershipFeatureClass = in_workspace + \
                                    "\\USFS_Ownership_LSRS\\2017_USFS_Ownership_CAALB83.gdb\\USFS_OwnershipLSRS_2017"

        intersectFeatureClass = outFeatClass + "_intersect"

        arcpy.AddMessage("Intersecting with USFS Ownership feature class .....")
        arcpy.AddMessage("Please be patient while this runs .....")

        if sys.version_info[0] < 3:
            arcpy.AddMessage("Python version of ArcGIS 10.x requires Intersect_analysis.")
            arcpy.AddMessage("Switch to ArcGIS Pro to use Pairwise Intersection and reduce runtime.")
            arcpy.Intersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)
        else:
            arcpy.PairwiseIntersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)

        arcpy.AddMessage("Completed Intersection")

        # CNDDB layer is skipped here because we need to remove BDF plants prior to exporting GDB
        if layerType != "CNDDB":
            # # may need to fix the NOAA layer - may remove this and just use the above
            # if layerType == "NOAA_ESU":
            #     copy_to_gdb("Interim", nameOfFile)
            # else:
            copy_to_gdb("Interim", intersectFeatureClass)

        dissolveFC = unitid_dissolve(intersectFeatureClass)

        # # may need to fix the NOAA layer - may remove this and just use the above
        # if layerType == "NOAA_ESU":
        #     copy_to_gdb("Final", dissolveFC)
        # else:
        copy_to_gdb("Final", dissolveFC)

    arcpy.AddMessage("Completed Script successfully!!")

except arcpy.ExecuteError:
    arcpy.AddError(arcpy.GetMessages(2))
except Exception as e:
    arcpy.AddMessage(e)


