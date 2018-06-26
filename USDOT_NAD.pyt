import arcpy
import csv


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [feature_count, domain_check, geometry_check]


class feature_count(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Feature Count"
        self.description = "This tool counts the total number of features within a feature class and produces a report with each field and their percent populated"
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""

	# Input Feature Class
	fc_in = arcpy.Parameter(
	    displayName="Input Featureclass",
	    name="input_featureclass",
	    datatype="DEFeatureClass",
	    parameterType="Required",
	    direction="Input")

	# Output Results File
	f_out = arcpy.Parameter(
	    displayName="Output Report",
	    name="output_report",
	    datatype="DEFile",
	    parameterType="Required",
	    direction="Output")

	f_out.value = ".csv"

        params = [fc_in, f_out]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
	fc_in = parameters[0].valueAsText
	f_out = parameters[1].valueAsText


	# Build the output csv
	f = csv.writer(open(f_out, 'wb'))

	row = ['Check', 'Count', 'Percentage']

	f.writerow(row)

	row = []

	result = arcpy.GetCount_management(fc_in)
	tot_count = int(result.getOutput(0))

	row = ['Total Feature Count', tot_count]

	f.writerow(row)

	row = []

	fields = arcpy.ListFields(fc_in)

	for field in fields:
	    if field.name <> "OBJECTID" and field.name <> "Shape":
	        if field.type == "String":
		    whereclause = field.name + " IS NOT NULL AND " + field.name + " <> ''"
	        else:
		    whereclause = field.name + " IS NOT NULL"
	        arcpy.MakeTableView_management(fc_in, "temp_view")
	        arcpy.SelectLayerByAttribute_management("temp_view", "NEW_SELECTION", whereclause)
	        pop_result = arcpy.GetCount_management("temp_view")
	        pop_count = int(pop_result.getOutput(0))
	        pop = float(pop_count)/float(tot_count)
	        row = [field.name,pop_count,pop]
	        f.writerow(row)
	        row = []
	        arcpy.Delete_management("temp_view") 

        return

class domain_check(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Domain Analysis"
        self.description = "This tool runs a frequency analysis on all of the domain related fields within the NAD feature class"
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""

	# Input Feature Class
	fc_input = arcpy.Parameter(
	    displayName="Input Featureclass",
	    name="input_featureclass",
	    datatype="DEFeatureClass",
	    parameterType="Required",
	    direction="Input")

	# Output Results File
	folder_out = arcpy.Parameter(
	    displayName="Output Folder",
	    name="output_folder",
	    datatype="DEFolder",
	    parameterType="Required",
	    direction="Input")

        params = [fc_input, folder_out]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
	fc_input = parameters[0].valueAsText
	folder_out = parameters[1].valueAsText

	# Local variables:
	frq_state_dbf = folder_out + "\\frq_state.dbf"
	frq_county_dbf = folder_out + "\\frq_county.dbf"
	frq_StN_PreDir_dbf = folder_out + "\\frq_StN_PreDir.dbf"
	frq_StN_PreTyp_dbf = folder_out + "\\frq_StN_PreTyp.dbf"
	frq_StN_PreSep_dbf = folder_out + "\\frq_StN_PreSep.dbf"
	frq_StN_PosTyp_dbf = folder_out + "\\frq_StN_PosTyp.dbf"
	frq_StN_PosDir_dbf = folder_out + "\\frq_StN_PosDir.dbf"
	frq_Addr_Type_dbf = folder_out + "\\frq_Addr_Type.dbf"
	frq_Placement_dbf = folder_out + "\\frq_Placement.dbf"

	arcpy.Frequency_analysis(fc_input, frq_state_dbf, "State", "")
	arcpy.Frequency_analysis(fc_input, frq_county_dbf, "County", "")
	arcpy.Frequency_analysis(fc_input, frq_StN_PreDir_dbf, "StN_PreDir", "")
	arcpy.Frequency_analysis(fc_input, frq_StN_PreTyp_dbf, "StN_PreTyp", "")
	arcpy.Frequency_analysis(fc_input, frq_StN_PreSep_dbf, "StN_PreSep", "")
	arcpy.Frequency_analysis(fc_input, frq_StN_PosTyp_dbf, "StN_PosTyp", "")
	arcpy.Frequency_analysis(fc_input, frq_StN_PosDir_dbf, "StN_PosDir", "")
	arcpy.Frequency_analysis(fc_input, frq_Addr_Type_dbf, "Addr_Type", "")
	arcpy.Frequency_analysis(fc_input, frq_Placement_dbf, "Placement", "")
	

	return

class geometry_check(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Check Geometry"
        self.description = "This tool runs a check geometry on the NAD feature class"
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""

	# Input Feature Class
	fc_input = arcpy.Parameter(
	    displayName="Input Featureclass",
	    name="input_featureclass",
	    datatype="DEFeatureClass",
	    parameterType="Required",
	    direction="Input")

	# Output Results File
	folder_out = arcpy.Parameter(
	    displayName="Output Folder",
	    name="output_folder",
	    datatype="DEFolder",
	    parameterType="Required",
	    direction="Input")

        params = [fc_input, folder_out]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
	fc_input = parameters[0].valueAsText
	folder_out = parameters[1].valueAsText

	# Local variables:
	check_geometry_dbf = folder_out + "\\check_geometry.dbf"

	arcpy.CheckGeometry_management(fc_input, check_geometry_dbf)

	return