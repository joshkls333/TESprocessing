# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# add_fields.py
# 
# Usage: add_fields 
# Description: Adds necessary fields for Fire Retardant processing
# Created by: Josh Klaus 07/27/2017
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import sys

in_workspace = sys.argv[1]

arcpy.env.workspace = in_workspace

intable = sys.argv[2]

# Process: Add Field
arcpy.AddField_management(intable, "UnitID", "TEXT", "", "", "5", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (2)
arcpy.AddField_management(intable, "GRANK_FIRE", "TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (3)
arcpy.AddField_management(intable, "SOURCEFIRE", "TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (4)
arcpy.AddField_management(intable, "SNAME_FIRE", "TEXT", "", "", "60", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (5)
arcpy.AddField_management(intable, "CNAME_FIRE", "TEXT", "", "", "60", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (6)
arcpy.AddField_management(intable, "BUFFT_FIRE", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (7)
arcpy.AddField_management(intable, "BUFFM_FIRE", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (8)
arcpy.AddField_management(intable, "CMNT_FIRE", "TEXT", "", "", "150", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (9)
arcpy.AddField_management(intable, "INST_FIRE", "TEXT", "", "", "150", "", "NULLABLE", "NON_REQUIRED", "")

