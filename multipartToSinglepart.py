# Name: MultipartToSinglepart_Example2.py
# Description: Break all multipart features into singlepart features,
#              and report which features were separated.
# Author: ESRI

# Import system modules
import arcpy
import numpy
import sys

# Create variables for the input and output feature classes

inFeatureClass = sys.argv[1]
#inFeatureClass = "c:/data/gdb.gdb/vegetation"
outFeatureClass = inFeatureClass + "_singlepart"

try:
    # Create list of all fields in inFeatureClass
    fieldNameList = [field.name for field in arcpy.ListFields(inFeatureClass)]

    # Add a field to the input this will be used as a unique identifier
    arcpy.AddField_management(inFeatureClass, "tmpUID", "double")

    # Determine what the name of the Object ID is
    OIDFieldName = arcpy.Describe(inFeatureClass).OIDFieldName

    # Calculate the tmpUID to the OID
    arcpy.CalculateField_management(inFeatureClass, "tmpUID",
                                    "[" + OIDFieldName + "]")

    # Run the tool to create a new fc with only singlepart features
    arcpy.MultipartToSinglepart_management(inFeatureClass, outFeatureClass)

    # Check if there is a different number of features in the output
    #   than there was in the input
    inCount = int(arcpy.GetCount_management(inFeatureClass).getOutput(0))
    outCount = int(arcpy.GetCount_management(outFeatureClass).getOutput(0))

    if inCount != outCount:
        # If there is a difference, print out the FID of the input
        #   features which were multipart
        arcpy.Frequency_analysis(outFeatureClass,
                                 outFeatureClass + "_freq", "tmpUID")

        # Use a search cursor to go through the table, and print the tmpUID
        print("Multipart features from {0}".format(inFeatureClass))
        for row in arcpy.da.SearchCursor(outFeatureClass + "_freq",
                                         ["tmpUID"], "FREQUENCY > 1"):
            print int(row[0])
    else:
        print("No multipart features were found")

except arcpy.ExecuteError:
    print arcpy.GetMessages()
except Exception as e:
    print e
