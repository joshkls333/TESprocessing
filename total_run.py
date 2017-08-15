# Import arcpy module
import arcpy
import sys
import csv
import os

# Set workspace or obtain from user input
in_workspace = r"C:\\Users\\jklaus\\Documents\\Python_Testing\\fire_retardant\\"
# in_workspace = sys.argv[1]

arcpy.env.workspace = in_workspace
arcpy.env.overwriteOutput = True

# selectQuery = sys.argv[3]

selectQuery = """ SCIENTIFIC_NAME = 'Acanthomintha ilicifolia' OR SCIENTIFIC_NAME = 'Acanthoscyphus parishii var. goodmaniana'
                  OR SCIENTIFIC_NAME = 'Allium munzii' OR SCIENTIFIC_NAME = 'Allium tribracteatum' OR SCIENTIFIC_NAME = 'Arabis johnstonii'
                  OR SCIENTIFIC_NAME = 'Arabis macdonaldiana' OR SCIENTIFIC_NAME = 'Arenaria ursina' OR SCIENTIFIC_NAME = 'Astragalus albens'
                  OR SCIENTIFIC_NAME = 'Astragalus brauntonii' OR SCIENTIFIC_NAME = 'Astragalus ertterae' OR SCIENTIFIC_NAME = 'Astragalus pachypus var. jaegeri'
                  OR SCIENTIFIC_NAME = 'Astragalus shevockii' OR SCIENTIFIC_NAME = 'Astragalus tricarinatus' OR SCIENTIFIC_NAME = 'Baccharis vanessae'
                  OR SCIENTIFIC_NAME = 'Berberis nevinii' OR SCIENTIFIC_NAME = 'Brodiaea filifolia' OR SCIENTIFIC_NAME = 'Castilleja cinerea'
                  OR SCIENTIFIC_NAME = 'Castilleja plagiotoma' OR SCIENTIFIC_NAME = 'Caulanthus californicus' OR SCIENTIFIC_NAME = 'Ceanothus ophiochilus'
                  OR SCIENTIFIC_NAME = 'Chorizanthe parryi var. parryi' OR SCIENTIFIC_NAME = 'Chorizanthe polygonoides ssp. longispina'
                  OR SCIENTIFIC_NAME = 'Clarkia springvillensis' OR SCIENTIFIC_NAME = 'Delphinium hesperium ssp. cuyamacae'
                  OR SCIENTIFIC_NAME = 'Dicentra nevadensis' OR SCIENTIFIC_NAME = 'Dodecahema leptoceras' OR SCIENTIFIC_NAME = 'Erigeron parishii'
                  OR SCIENTIFIC_NAME = 'Eriogonum breedlovei var. breedlovei' OR SCIENTIFIC_NAME = 'Eriogonum kennedyi var. austromontanum'
                  OR SCIENTIFIC_NAME = 'Eriogonum ovalifolium var. vineum' OR SCIENTIFIC_NAME = 'Eriogonum spectabile' OR SCIENTIFIC_NAME = 'Horkelia tularensis'
                  OR SCIENTIFIC_NAME = 'Imperata brevifolia' OR SCIENTIFIC_NAME = 'Leptosiphon floribundum ssp. hallii' OR SCIENTIFIC_NAME = 'Lupinus constancei'
                  OR SCIENTIFIC_NAME = 'Monardella macrantha ssp. hallii' OR SCIENTIFIC_NAME = 'Monardella viridis ssp. saxicola'
                  OR SCIENTIFIC_NAME = 'Nemacladus twisselmannii' OR SCIENTIFIC_NAME = 'Orcuttia tenuis' OR SCIENTIFIC_NAME = 'Oreonana vestita'
                  OR SCIENTIFIC_NAME = 'Penstemon californicus' OR SCIENTIFIC_NAME = 'Phlox hirsuta' OR SCIENTIFIC_NAME = 'Physaria kingii ssp. bernardina'
                  OR SCIENTIFIC_NAME = 'Lesquerella kingii ssp. bernardina' OR SCIENTIFIC_NAME = 'Poa atropurpurea' OR SCIENTIFIC_NAME = 'Pseudobahia peirsonii'
                  OR SCIENTIFIC_NAME = 'Packera layneae' OR SCIENTIFIC_NAME = 'Sidalcea hickmanii ssp. parishii' OR SCIENTIFIC_NAME = 'Sidalcea keckii'
                  OR SCIENTIFIC_NAME = 'Sidalcea pedata' OR SCIENTIFIC_NAME = 'Streptanthus cordatus var. piutensis' OR SCIENTIFIC_NAME = 'Streptanthus fenestratus'
                  OR SCIENTIFIC_NAME = 'Taraxacum californicum' OR SCIENTIFIC_NAME = 'Thelypodium stenopetalum' OR SCIENTIFIC_NAME = 'Thelypteris puberula var. sonorensis'
                  OR SCIENTIFIC_NAME = 'Trifolium dedeckerae' OR SCIENTIFIC_NAME = 'Tuctoria greenei' OR SCIENTIFIC_NAME = 'Howellia aquatilis'
                  OR SCIENTIFIC_NAME = 'Heterotheca shevockii' OR SCIENTIFIC_NAME = 'Marina orcuttii var. orcuttii'
                  OR ACCEPTED_SCIENTIFIC_NAME = 'Mahonia nevinii' OR ACCEPTED_SCIENTIFIC_NAME = 'Stanfordia californica' OR ACCEPTED_SCIENTIFIC_NAME = 'Clarkia springvillensis'
                  OR ACCEPTED_SCIENTIFIC_NAME = 'Abronia alpina' OR ACCEPTED_SCIENTIFIC_NAME = 'Calochortus persistens' """

# selection = sys.argv[3].split(',')

tl = """Acanthomintha ilicifolia,Arenaria ursina,Astragalus tricarinatus,
        Baccharis vanessae,Brodiaea filifolia,
        Castilleja cinerea,Ceanothus ophiochilus,Eriogonum kennedyi var. austromontanum,
        Orcuttia tenuis,Pseudobahia peirsonii,Howellia aquatilis"""


sl = """Allium tribracteatum,Arabis johnstonii,Astragalus ertterae,Astragalus pachypus var. jaegeri,Astragalus shevockii,Castilleja plagiotoma,
        Chorizanthe parryi var. parryi,Chorizanthe polygonoides ssp. longispina,Delphinium hesperium ssp. cuyamacae,Dicentra nevadensis,
        riogonum breedlovei var. breedlovei,Eriogonum spectabile,Lupinus constancei,Monardella macrantha ssp. hallii,
        Monardella viridis ssp. saxicola,Nemacladus twisselmannii,Oreonana vestita,Penstemon californicus,Streptanthus cordatus var. piutensis,
        Streptanthus fenestratus,Thelypteris puberula var. sonorensis,Trifolium dedeckerae,Sidalcea hickmanii ssp. parishii,Heterotheca shevockii,
        Horkelia tularensis, Marina orcuttii var. orcuttii"""

threatenedList = tl.split(',')
sensitiveList = sl.split(',')

# threatenedList = sys.argv[4].split(',')
# sensitiveList = sys.argv[5].split(',')

newpath_threatened = in_workspace + "2017_Threatened"
threatened_gdb = "2017_FRA_Threatened_OriginalDataNoBuffers_FWSDeliverable_CAALAB83.gdb"
newpath_endangered = in_workspace + "2017_Endangered"
endangered_gdb = "2017_FRA_Endangered_OriginalDataNoBuffers_FWSDeliverable_CAALAB83.gdb"
newpath_sensitive  = in_workspace + "2017_Sensitive"
sensitive_gdb = "2017_FRA_Sensitive_OriginalDataNoBuffers_FWSDeliverable_CAALAB83.gdb"

if not os.path.exists(newpath_sensitive):
    arcpy.AddMessage("Creating directory for Sensitive Data Deliverables ....")
    os.makedirs(newpath_sensitive)

arcpy.AddMessage("Creating Geodatabase for Sensitive Data Deliverables ....")
arcpy.CreateFileGDB_management(newpath_sensitive, sensitive_gdb)

if not os.path.exists(newpath_endangered):
    arcpy.AddMessage("Creating directory for Endangered Data Deliverables ....")
    os.makedirs(newpath_endangered)

arcpy.AddMessage("Creating Geodatabase for Endangered Data Deliverables ....")
arcpy.CreateFileGDB_management(newpath_endangered, endangered_gdb)

if not os.path.exists(newpath_threatened):
    arcpy.AddMessage("Creating directory for Threatened Data Deliverables ....")
    os.makedirs(newpath_threatened)

arcpy.AddMessage("Creating Geodatabase for Threatened Data Deliverables ....")
arcpy.CreateFileGDB_management(newpath_threatened, threatened_gdb)

intable = in_workspace + "\\2017_EDW_CAALB83.gdb\\EDW_TESP_2017_OccurrenceAll_FoundPlants"
# intable = sys.argv[2]

outtable = intable + "_complete"

#csvFile = sys.argv[6]
csvFile = r"C:\\Users\\jklaus\\Documents\\Python_Testing\\fire_retardant\\TESP_SummaryTable.csv"

try:

    arcpy.MakeFeatureLayer_management(intable, "lyr" )

    arcpy.AddMessage("-----------------")
    arcpy.AddMessage("Selection: " + selectQuery)
    arcpy.AddMessage("-----------------")

    arcpy.AddMessage("Selecting layers based on selection ....")
    arcpy.SelectLayerByAttribute_management ("lyr", "NEW_SELECTION", selectQuery )

    # selectQuery = 'SCIENTIFIC_NAME = '
    # selectQuery += ' OR SCIENTIFIC_NAME = '.join(selection)

    arcpy.AddMessage("Copying selected records to new feature ......")
    arcpy.CopyFeatures_management("lyr", outtable)

    result = arcpy.GetCount_management(outtable)
    count = int(result.getOutput(0))
    arcpy.AddMessage("Total Number of Records: " + str(count))

    cur = arcpy.UpdateCursor(outtable)
    threatNum = 0
    sensitiveNum = 0
    endangerNum = 0

    field = "SCIENTIFIC_NAME"
    field2 = "ACCEPTED_COMMON_NAME"
    arcpy.AddMessage("Populating attributes .....")

    for row in cur:
        speciesrow = row.getValue(field)
        buffer_amount = 1

        row.SOURCEFIRE = "EDW TESp OccurrencesALL_FoundPlant pulled 2/2017"
        row.SNAME_FIRE = speciesrow
        row.CNAME_FIRE = row.getValue(field2)

        with open(csvFile) as f:
            reader = csv.reader(f)
            for line in reader:

                species = line[0]
                status = line[1]
                buff = line[2]

                if species.startswith(speciesrow) and status != "CH":

                    if buff == "NN" or "":
                            buffer_amount = 0
                    else:
                            buffer_amount = int(buff)
                    break
        row.BUFFT_FIRE = buffer_amount
        row.BUFFM_FIRE = buffer_amount * 0.3048

        if row.getValue(field) in threatenedList :
            row.GRANK_FIRE = "Threatened"
            threatNum += 1
        elif row.getValue(field) in sensitiveList:
            row.GRANK_FIRE = "Sensitive"
            sensitiveNum += 1
        else:
            row.GRANK_FIRE = "Endangered"
            endangerNum += 1
        cur.updateRow(row)

    arcpy.AddMessage("Number of Threatened = " + str(threatNum))
    arcpy.AddMessage("Number of Sensitive = " + str(sensitiveNum))
    arcpy.AddMessage("Number of Endangered = " + str(endangerNum))

    del cur

    arcpy.AddMessage("Splitting current state of data into deliverable Geodatabases .....")

#    does not work in ArcGIS only ArcGIS Pro
#    arcpy.SplitByAttributes_analysis(outtable, sensitive_gdb, "GRANK_FIRE")

#    status_fc = intable + "_noAAAbuf"

##    Work on a way to take the three copy sections to GDB and place in a function
##    __________________________________________________________________________________________________
###--------------Copying to Sensitive Geodatabase for interim deliverable step
    arcpy.MakeFeatureLayer_management(outtable, "lyr" )

    arcpy.AddMessage("Selecting layers based on selection ....")
    arcpy.SelectLayerByAttribute_management ("lyr", "NEW_SELECTION", "GRANK_FIRE = 'Sensitive'" )

    outlocation = newpath_sensitive + "\\\\" + sensitive_gdb + "\\\\EDW_TESP_2017_Sensitive_OccurrenceAll_FoundPlants_nobuf"

    arcpy.AddMessage("Copying selected records to Sensitive Geodatabase ......")
    arcpy.CopyFeatures_management("lyr", outlocation)

    result = arcpy.GetCount_management(outlocation)
    count = int(result.getOutput(0))
    arcpy.AddMessage("Total Number of Records: " + str(count))

###--------------Copying to Threatened Geodatabase for interim deliverable step

    arcpy.MakeFeatureLayer_management(outtable, "lyr" )

    arcpy.AddMessage("Selecting layers based on selection ....")
    arcpy.SelectLayerByAttribute_management ("lyr", "NEW_SELECTION", "GRANK_FIRE = 'Threatened'" )

    outlocation = newpath_threatened + "\\\\" + threatened_gdb + "\\\\EDW_TESP_2017_Threatened_OccurrenceAll_FoundPlants_nobuf"

    arcpy.AddMessage("Copying selected records to Threatened Geodatabase ......")
    arcpy.CopyFeatures_management("lyr", outlocation)

    result = arcpy.GetCount_management(outlocation)
    count = int(result.getOutput(0))
    arcpy.AddMessage("Total Number of Threatened Records: " + str(count))

###--------------Copying to Endangered Geodatabase for interim deliverable step
    arcpy.MakeFeatureLayer_management(outtable, "lyr" )

    arcpy.AddMessage("Selecting layers based on selection ....")
    arcpy.SelectLayerByAttribute_management ("lyr", "NEW_SELECTION", "GRANK_FIRE = 'Endangered'" )

    outlocation = newpath_endangered + "\\\\" + endangered_gdb + "\\\\EDW_TESP_2017_Endangered_OccurrenceAll_FoundPlants_nobuf"

    arcpy.AddMessage("Copying selected records to Endangered Geodatabase ......")
    arcpy.CopyFeatures_management("lyr", outlocation)

    result = arcpy.GetCount_management(outlocation)
    count = int(result.getOutput(0))
    arcpy.AddMessage("Total Number of Endangered Records: " + str(count))

##    __________________________________________________________________________________________________


##----------------------------------------------------------------------
## Tested below pieces - commenting out to test attribution
##----------------------------------------------------------------------
    outFeatureClass = outtable + "_singlepart"

    arcpy.AddMessage("Converting multipart geometry to singlepart .....")

    arcpy.MultipartToSinglepart_management(outtable, outFeatureClass)

    inCount = int(arcpy.GetCount_management(outtable).getOutput(0))
    outCount = int(arcpy.GetCount_management(outFeatureClass).getOutput(0))

    arcpy.AddMessage("Number of new records: " + str(outCount - inCount))

    arcpy.AddMessage("Repairing Geometry ......")
    arcpy.RepairGeometry_management(outFeatureClass)

    arcpy.AddMessage("Buffering features ....")
    buffer_fc = outFeatureClass + "_buffer"
    buffer_field = "BUFFM_FIRE"
    arcpy.Buffer_analysis(outFeatureClass, buffer_fc, buffer_field)

    outFeatClass = buffer_fc + "_spart"

    arcpy.AddMessage("Converting buffer layer from multipart geometry to singlepart .....")

    arcpy.MultipartToSinglepart_management(buffer_fc, outFeatClass)

    inCount = int(arcpy.GetCount_management(buffer_fc).getOutput(0))
    outCount = int(arcpy.GetCount_management(outFeatClass).getOutput(0))

    arcpy.AddMessage("Number of new records: " + str(outCount - inCount))

    arcpy.AddMessage("Repairing Geometry of singlepart buffer layer ......")
    arcpy.RepairGeometry_management(outFeatClass)


## -------------
#   Please note everything above here comes from select_tes_layer.py
## -------------

##-----------------------------------------------------------------------------------
    # Note this process will be run in another script within an ArcGIS Pro environment using PairwiseIntersect_analysis
    # arcpy.Intersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)
    # arcpy.PairwiseIntersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)
##-----------------------------------------------------------------------------------

    usfsOwnershipFeatureClass = r"C:\Users\jklaus\Documents\Python_Testing\fire_retardant\USFS_Ownership_LSRS\2017_USFS_Ownership_CAALB83.gdb\USFS_OwnershipLSRS_2017"

    intersectFeatureClass = outFeatClass + "_intersect"

    arcpy.AddMessage("Intersecting with USFS Ownership feature class .....")
    arcpy.AddMessage("Please be patient while this runs .....")
    # arcpy.Intersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)
    arcpy.PairwiseIntersect_analysis([outFeatClass, usfsOwnershipFeatureClass], intersectFeatureClass)

    arcpy.AddMessage("Intersection complete seperating data out to Geodatabases for deliverables ......")

##    Work on a way to take the three copy sections to GDB and place in a function
##    __________________________________________________________________________________________________
###--------------Copying to Sensitive Geodatabase for interim deliverable step
    arcpy.MakeFeatureLayer_management(intersectFeatureClass, "lyr" )

    arcpy.AddMessage("Selecting layers based on selection ....")
    arcpy.SelectLayerByAttribute_management ("lyr", "NEW_SELECTION", "GRANK_FIRE = 'Sensitive'" )

    outlocation = newpath_sensitive + "\\\\" + sensitive_gdb + "\\\\EDW_TESP_2017_Sensitive_OccurrenceAll_FoundPlants_ident"

    arcpy.AddMessage("Copying selected records to Sensitive Geodatabase ......")
    arcpy.CopyFeatures_management("lyr", outlocation)

    result = arcpy.GetCount_management(outlocation)
    count = int(result.getOutput(0))
    arcpy.AddMessage("Total Number of Records: " + str(count))

###--------------Copying to Threatened Geodatabase for interim deliverable step

    arcpy.MakeFeatureLayer_management(intersectFeatureClass, "lyr" )

    arcpy.AddMessage("Selecting layers based on selection ....")
    arcpy.SelectLayerByAttribute_management ("lyr", "NEW_SELECTION", "GRANK_FIRE = 'Threatened'" )

    outlocation = newpath_threatened + "\\\\" + threatened_gdb + "\\\\EDW_TESP_2017_Threatened_OccurrenceAll_FoundPlants_ident"

    arcpy.AddMessage("Copying selected records to Threatened Geodatabase ......")
    arcpy.CopyFeatures_management("lyr", outlocation)

    result = arcpy.GetCount_management(outlocation)
    count = int(result.getOutput(0))
    arcpy.AddMessage("Total Number of Threatened Records: " + str(count))

###--------------Copying to Endangered Geodatabase for interim deliverable step
    arcpy.MakeFeatureLayer_management(intersectFeatureClass, "lyr" )

    arcpy.AddMessage("Selecting layers based on selection ....")
    arcpy.SelectLayerByAttribute_management ("lyr", "NEW_SELECTION", "GRANK_FIRE = 'Endangered'" )

    outlocation = newpath_endangered + "\\\\" + endangered_gdb + "\\\\EDW_TESP_2017_Endangered_OccurrenceAll_FoundPlants_ident"

    arcpy.AddMessage("Copying selected records to Endangered Geodatabase ......")
    arcpy.CopyFeatures_management("lyr", outlocation)

    result = arcpy.GetCount_management(outlocation)
    count = int(result.getOutput(0))
    arcpy.AddMessage("Total Number of Endangered Records: " + str(count))

##    __________________________________________________________________________________________________


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
                  "BASICOWNERSHIPID", "OWNERCLASSIFICATION", "GIS_ACRES_1", "REGION", "REGION_1",
                  "FORESTNAME", "FORESTNAME_1", "FID_USFS_OwnershipLSRS_2017", "ORIG_FID", "AREA_OCCUPANCY",
                  "COMMON_NAME", "SCIENTIFIC_NAME", "ACCEPTED_COMMON_NAME", "ACCEPTED_SCIENTIFIC_NAME",
                  "SITE_ID_FS", "FID_EDW_TESP_2017_OccurrenceAll_Found"]

    # Execute CopyFeatures to make a new copy of the feature class
    # Use CopyRows if you have a table

    arcpy.CopyFeatures_management(inFeatures, outFeatureClass)

    arcpy.AddMessage("Deleting all unnecessary fields ......")
    # Execute DeleteField
    arcpy.DeleteField_management(outFeatureClass, dropFields)

    arcpy.AddMessage("Repairing Geometry ......")
    arcpy.RepairGeometry_management(outFeatureClass)

    cur = arcpy.UpdateCursor(outFeatureClass)

    field = "UnitID_FS"

    for row in cur:
        row.UnitID = "0" + row.getValue(field)
        cur.updateRow(row)

    del cur



except arcpy.ExecuteError:
    arcpy.GetMessages()
except Exception as e:
    arcpy.AddMessage(e)
